# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a local provenance-checking web service that evaluates submitted text using two independent signals—a causal language model perplexity signal and a surface stylometry signal—combines them into a single confidence score, maps that score to a human-readable provenance label, logs every decision to an append-only JSONL audit trail, and provides an appeal endpoint for writers to contest false positives.

### End-to-End Submission Path (7 Steps)

1. **HTTP Arrival & Input Validation (`app.py::submit`, `POST /submit`):** A client sends a JSON payload (`{"text": "...", "creator_id": "..."}`). The route parses the JSON, validates that `text` is a non-empty string within length bounds (logging a rejection via `audit.log_rejection` and returning `400 Bad Request` if missing, too short, or oversized), normalizes `creator_id` (defaulting to `"anonymous"` if omitted), and mints a unique `content_id` (`uuid4`).
2. **Signal One — Model Predictability (`detector.py::model_signal`):** The validated text passes through the local `gpt2` causal language model (`perplexity(text)`), which computes the exponential of mean token-level cross-entropy loss (up to `DETECTOR_MAX_TOKENS = 400` tokens) and squashes it via a logistic curve (`midpoint = 45.0`, `steepness = 1.6`) into `model_score` in `[0.0, 1.0]`, adding a measure of how predictable the word sequence is (`1.0` = highly predictable / AI-like).
3. **Signal Two — Surface Stylometry (`stylometry.py::style_signal`):** In parallel, the raw text passes through `stylometry.py`, which tokenizes sentences and words without reading semantics to compute `sentence_length_spread`, `type_token_ratio`, and `punctuation_density`, combining and scaling them into `style_score` in `[0.0, 1.0]` (`1.0` = uniform sentence cadence, repetitive vocabulary, and flat punctuation typical of unedited AI output).
4. **Signal Combination (`scoring.py::combine_signals`):** Both `model_score` and `style_score` are passed to `combine_signals(model_score, style_score)`, which merges them into a single `combined_score` (`confidence`) in `[0.0, 1.0]` according to our weighting rule.
5. **Threshold & Human-Readable Label Mapping (`scoring.py::score_to_label`):** `score_to_label(combined_score)` compares the combined score against `config.HUMAN_THRESHOLD` and `config.AI_THRESHOLD`, adding both a short machine-readable `guess` (`"human"`, `"unsure"`, or `"ai"`) and the exact plain-English `label` string that a reader or writer sees.
6. **Append-Only Audit Logging (`audit.py::log_decision`):** Before responding, the service writes a permanent, timestamped JSON line to `logs/audit.jsonl` containing all nine required audit fields (`timestamp`, `content_id`, `creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `label`, and `status = "decided"`).
7. **JSON Response & Appeal Lifecycle (`app.py::submit` → `POST /appeal`):** The route returns HTTP `200 OK` with `content_id`, `guess`, `confidence`, `label`, `model_score`, and `style_score`. If the writer disagrees with the label, they submit `content_id` and `reasoning` to `POST /appeal` (`app.py::appeal`), which verifies `content_id` via `audit.entries_for(content_id)` and appends an `"under_review"` appeal record via `audit.log_appeal`.

### Tracing the False Positive

- **Who submits and why it happens:** A real human writer—for example, a second-language English speaker or a technical writer who deliberately writes in short, direct sentences using familiar, high-frequency words—submits their own original paragraph to `POST /submit`.
- **What scores they get:** Because their vocabulary is simple and their sentence transitions follow standard grammatical patterns, `gpt2` is rarely surprised (`perplexity ≈ 22`), producing a high `model_score` (e.g., `0.76`). Because their sentences are uniformly short (`12–15` words) with only periods and commas, `style_score` also lands high (e.g., `0.68`), yielding a combined `confidence` score of `0.72`—above `AI_THRESHOLD` (`0.65`).
- **What the label says to them:** Their response comes back with `"guess": "ai"` and a `label` stating: *"This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID."*
- **What they can do about it:** Using the `content_id` returned in their `POST /submit` response, the writer sends a `POST /appeal` request with `{"content_id": "<their-content-id>", "reasoning": "I wrote this myself in plain English; I can provide my draft history."}`. The service verifies that `content_id` exists in `logs/audit.jsonl`, appends a new log entry with `"event": "appeal"` and `"status": "under_review"` alongside the original decision, and returns confirmation that their work has been placed `under_review` rather than leaving an unchallengeable accusation on record.

### Endpoint Contracts

#### 1. `POST /submit`

- **Request (`application/json`):**
  | Field          | Type       | Required                         | Description                                                                                                                 |
  | -------------- | ---------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
  | `text`       | `string` | Yes                              | The text submission to evaluate (must contain at least 3 tokens / a few sentences and not exceed maximum character limits). |
  | `creator_id` | `string` | No (defaults to `"anonymous"`) | Identifier for the submitting writer or account.                                                                            |
- **Success Response (`200 OK`, `application/json`):**
  | Field           | Type       | Description                                                                                                     |
  | --------------- | ---------- | --------------------------------------------------------------------------------------------------------------- |
  | `content_id`  | `string` | Unique identifier (`uuid4` hex/string) generated for this submission, used to look up or appeal the decision. |
  | `guess`       | `string` | Machine-readable classification: `"human"`, `"unsure"`, or `"ai"`.                                        |
  | `confidence`  | `float`  | Combined score in `[0.0, 1.0]` output by `scoring.combine_signals` (`0.0` = human, `1.0` = AI).         |
  | `label`       | `string` | Plain-English sentence shown to the reader/writer (from `scoring.score_to_label`).                            |
  | `model_score` | `float`  | Signal 1 score in `[0.0, 1.0]` from `detector.model_signal`.                                                |
  | `style_score` | `float`  | Signal 2 score in `[0.0, 1.0]` from `stylometry.style_signal`.                                              |
  | `status`      | `string` | Initial lifecycle state: `"decided"`.                                                                         |
- **Error Response (`400 Bad Request` / `429 Too Many Requests`, `application/json`):**
  Returns `{"error": "<reason_code>", "message": "<human-readable explanation>"}` and records a `"rejected"` entry in `logs/audit.jsonl`.

#### 2. `POST /appeal`

- **Request (`application/json`):**
  | Field          | Type       | Required | Description                                                      |
  | -------------- | ---------- | -------- | ---------------------------------------------------------------- |
  | `content_id` | `string` | Yes      | The `content_id` returned by an earlier `POST /submit` call. |
  | `reasoning`  | `string` | Yes      | The writer's explanation contesting the classification.          |
- **Success Response (`200 OK`, `application/json`):**
  | Field          | Type       | Description                                                           |
  | -------------- | ---------- | --------------------------------------------------------------------- |
  | `content_id` | `string` | The appealed submission's `content_id`.                             |
  | `creator_id` | `string` | The `creator_id` associated with the original submission.           |
  | `status`     | `string` | Updated lifecycle status: `"under_review"`.                         |
  | `reasoning`  | `string` | Echo of the writer's submitted appeal reasoning.                      |
  | `message`    | `string` | Confirmation message to the writer that their appeal has been logged. |
- **Error Response (`400 Bad Request` / `404 Not Found`, `application/json`):**
  Returns `400` if `content_id` or `reasoning` is missing/blank, or `404` (`{"error": "not_found", "message": "..."}`) if `audit.entries_for(content_id)` finds no matching submission.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Token-level **perplexity** (next-token predictability) under a local causal language model (`gpt2` in `detector.py::model_signal`), transformed via a logistic curve (`midpoint = 45.0`, `steepness = 1.6`) into a `0.0–1.0` score where higher values indicate lower perplexity (more predictable text).

**Why that might differ between human and AI writing:**
Autoregressive language models generate text by sampling high-probability next tokens at every step, so unedited AI prose tends to follow smooth, high-likelihood word transitions that `gpt2` predicts with low surprise (low perplexity → high `model_score`). Human writers make idiosyncratic word choices, abrupt topic jumps, and specific concrete references that surprise a general language model (high perplexity → low `model_score`).

**What it can't see:**
Predictability is not authorship: `model_signal` cannot distinguish between machine generation and **a real human writing plainly in common words and short, straightforward sentences** (such as an L2/non-native English speaker, a young student, or a concise technical writer), whom it falsely flags as AI. Conversely, it is easily fooled in the opposite direction by AI text prompted to use rare, ornate vocabulary or injected with deliberate typos/unusual tokens, which spike `gpt2` perplexity and make AI text look human.

### Signal two — the style signal

**What it measures:**
Surface **structural and lexical regularity** of the text (`stylometry.py::style_signal`), combining three non-semantic measures:

1. `sentence_length_spread`: coefficient of variation (standard deviation divided by mean) of sentence word counts.
2. `type_token_ratio`: ratio of unique lowercase words to total words (lexical diversity).
3. `punctuation_density`: frequency and variety of expressive punctuation (commas, semicolons, dashes, parentheses, exclamation/question marks) relative to word count.

**Why that might differ between human and AI writing:**
Default LLM outputs tend to march in uniform, medium-length sentences (`15–22` words) with low sentence-length variance, reuse safe transition words, and rely almost exclusively on standard periods and commas. Human prose is naturally bursty and lumpy—mixing a three-word fragment next to a forty-word clause (`high sentence_length_spread`), using more varied vocabulary in short passages, and employing idiosyncratic punctuation (dashes, parentheticals, semicolons, exclamation marks).

**What it can't see:**
`style_signal` **cannot read a single word for meaning or grammar**. Any cheap surface perturbation that alters character or sentence shapes without changing the underlying AI-generated content—such as splitting one sentence with a period to create a 2-word fragment, sprinkling random typos (which inflate unique word counts in `type_token_ratio`), or inserting dummy semicolons/dashes—fools `style_signal` into scoring AI text as human. Conversely, a human writing a structured list or a single-sentence submission has near-zero sentence-length spread and can be misread as machine-like.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
Our combining rule takes an equally-weighted combination (50/50) of the semantic predictability score (`model_score`) and surface structural burstiness (`style_score`). When both signals corroborate each other (e.g. low perplexity and low structural burstiness), the combined score reaches decisive confidence. When the two signals disagree (e.g. one signal reads human while the other reads machine), their average falls into the intermediate "unsure" decision band (0.35 to 0.65). By requiring consensus between both independent signals before making a high-confidence AI accusation, this rule directly limits false-positive accusations against human writers whose texts trigger only one signal (e.g., uniform formatting or familiar, predictable wording).

**The numbers:**
- `WEIGHT_MODEL_SIGNAL = 0.5` (defined in `config.py`)
- `WEIGHT_STYLE_SIGNAL = 0.5` (defined in `config.py`)
- `HUMAN_THRESHOLD = 0.35` (defined in `config.py`)
- `AI_THRESHOLD = 0.65` (defined in `config.py`)
- Combining formula: `combined_score = round(0.5 * model_score + 0.5 * style_score, 4)`
- Decision boundaries:
  - `combined_score <= 0.35` -> `"human"`
  - `0.35 < combined_score < 0.65` -> `"unsure"`
  - `combined_score >= 0.65` -> `"ai"`

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
- **Input Text:**
  > *"Hi team, please find attached the meeting notes from yesterday's sync. We reviewed the quarterly roadmap and finalized our delivery schedule. The design review is postponed until next Tuesday due to conference travel. Let me know if you have any feedback before tomorrow afternoon."*
- **Signal Breakdown:**
  - `model_score = 0.3839` (Perplexity 58.2 under GPT-2; domain terms like "sync", "roadmap", and "postponed" cause enough token-level surprise to keep the score close to human).
  - `style_score = 0.7808` (Sentence lengths are uniform at 11, 10, 11, and 10 words, with no semicolons, em dashes, or expressive punctuation marks, which `style_signal` views as AI-like).
- **How the combining rule handles it:**
  `combine_signals(0.3839, 0.7808)` outputs `0.5824`. Because `0.5824` sits inside the `(0.35, 0.65)` range, the service returns `"guess": "unsure"`. Rather than convicting the writer based on flat formatting alone, the rule recognises that disagreement signifies uncertainty, protecting the writer from a false positive.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range | The exact text a reader sees |
| --------------------- | ----------- | ---------------------------- |
| high-confidence human | 0.00 – 0.35 | We're confident this text was written by a person, showing the natural variety and pacing of human expression. |
| unsure                | 0.35 – 0.65 | We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call. |
| high-confidence AI    | 0.65 – 1.00 | This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID. |

**Why I worded the "unsure" one this way:**
The "unsure" label is intentionally framed around the service's own observational boundaries ("We can't tell", "we are not making an automated call") rather than making an accusatory or suspicious claim about the author ("questionable text", "unverified origin"). Real human writing varies tremendously—from concise emails to structured technical documentation—and frequently exhibits uniform cadence or simple vocabulary that triggers intermediate scores. By transparently acknowledging that the text exhibits mixed characteristics and refusing to guess or assign a punitive classification, the label protects writers from unjustified suspicion while remaining honest about the limits of multi-signal heuristics.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "test_ai"}'
```

```json
{
  "confidence": 0.857,
  "content_id": "8544a988-9007-40c2-8a0d-75a9caa52827",
  "guess": "ai",
  "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
  "model_score": 0.8864,
  "status": "decided",
  "style_score": 0.8277
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "8544a988-9007-40c2-8a0d-75a9caa52827", "reasoning": "I wrote this paragraph myself for an academic report on systems architecture. Please review."}'
```

```json
{
  "content_id": "8544a988-9007-40c2-8a0d-75a9caa52827",
  "creator_id": "test_ai",
  "message": "Your appeal has been received and this submission is now under review.",
  "reasoning": "I wrote this paragraph myself for an academic report on systems architecture. Please review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "content_id": "6317b6e1-f847-4c85-83cd-90ffa9600f33",
      "creator_id": "ai_test",
      "event": "appeal",
      "reasoning": "I wrote this paragraph myself for an academic report on systems architecture. Please review.",
      "status": "under_review",
      "timestamp": "2026-11-04T23:45:56+00:00"
    },
    {
      "combined_score": 0.857,
      "content_id": "8544a988-9007-40c2-8a0d-75a9caa52827",
      "creator_id": "test_ai",
      "guess": "ai",
      "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": 0.8277,
      "timestamp": "2026-11-04T23:46:46+00:00"
    },
    {
      "content_id": "8544a988-9007-40c2-8a0d-75a9caa52827",
      "creator_id": "test_ai",
      "event": "appeal",
      "reasoning": "I wrote this paragraph myself for an academic report on systems architecture. Please review.",
      "status": "under_review",
      "timestamp": "2026-11-04T23:46:46+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
  Guidance on designing and combining the surface stylometric metrics (sentence length variance, type-token ratio, and punctuation density) in `stylometry.py` so they point in the same direction as `model_signal` (`1.0` = AI, `0.0` = human) and stay bounded in `[0.0, 1.0]`.
- *What came back:*
  A raw formula that summed the unscaled standard deviation of sentence lengths and an unbounded count of total punctuation marks, alongside a suggestion to assign a maximal AI score (`1.0`) if a submission contained only one sentence.
- *What I changed:*
  I replaced the raw standard deviation with the coefficient of variation (CV = stdev / mean) so short and long submissions could be evaluated on a scale-independent basis. I restricted punctuation counting to expressive/structural punctuation (semicolons, dashes, parentheses, exclamation and question marks) normalized by word count. For single-sentence submissions, I set sentence spread to a neutral `0.5` rather than `1.0` to avoid penalizing short human notes. Finally, I calibrated linear clamp intervals to map each feature smoothly onto $[0.0, 1.0]$.

**Moment 2**

- *What I asked for:*
  Drafting reader-facing text for the three classification labels (`high-confidence human`, `unsure`, and `high-confidence AI`) that communicates clearly to a lay reader without using statistical or engineering terms like "threshold" or "confidence score".
- *What came back:*
  Formal, technical labels such as *"Classification: human, 0.81 confidence"*, *"Unverified text: cannot determine authenticity"*, and *"Flagged as AI generated prose"*.
- *What I changed:*
  I rewrote all three labels into conversational, plain-English sentences. Crucially, I overhauled the "unsure" label: instead of describing the text as "unverified" or "suspicious", I reframed it around the system's own observational limits (*"We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call."*). This prevents alienating human writers who submit concise, structured prose.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
A genuine writer works iteratively, drafting and revising text at a natural pace of a few submissions an hour. Even in active burst editing or classroom review sessions, a writer will not submit more than 10 drafts in a single minute or 200 in a single day. Conversely, an adversary trying to map detector thresholds or brute-force evasions relies on high-throughput automated scripting across hundreds or thousands of prompt variations. A 10/minute rate limit makes high-volume reconnaissance prohibitively slow (mapping 1,000 variations would take over an hour and a half) and quickly trips the 200/day limit, neutralizing automated threshold exploration while remaining completely transparent to human users.

**What a caller counts as:** 
A caller counts as their `creator_id` provided in the JSON body (`payload.get("creator_id")`). If `creator_id` is omitted, blank, or the payload is not a valid JSON object, the limiter safely falls back to the caller's remote IP address (`flask_limiter.util.get_remote_address`).

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `88112a26-1133-4d8b-b76c-7b2289c34a58` | unsure | 0.486 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `3951be86-3d00-4154-8f6e-7437a618aa8a` | unsure | 0.509 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c92738a2-64d7-4c0b-8afc-f31ef2b94c01` | unsure | 0.510 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `0331ee25-1df1-430a-8a2f-57213224dd89` | ai | 0.682 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `9da0839d-6939-47ed-bd1c-94931ff63135` | human | 0.325 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `be4b4624-f9f7-40f3-a3c1-5668799c99c2` | unsure | 0.539 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `891f6b59-77b6-46c9-8f49-2d02a5890c77` | unsure | 0.472 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `18b269d6-1bd7-40bd-80e7-566121e13cd8` | unsure | 0.448 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `e95640d9-cd54-4280-8c26-fb71506e1a8b` | unsure | 0.519 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `94e3d7b6-2ae1-40bd-954d-6bac3cf3d669` | ai | 0.852 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `be07ef34-ab48-4b2d-bc81-b8f7550f7e6d` | unsure | 0.632 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c48462d1-1fa7-4f1b-a7b8-ffc53201df5d` | ai | 0.814 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `3e484177-a020-46b1-80c6-b269af00fb1b` | ai | 0.792 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `e20301a8-65f1-4383-97b4-7f5dfabecc8d` | ai | 0.745 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `2275aba4-95cf-4449-a2bd-d096fc186689` | ai | 0.829 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `9ad4f32b-be77-4077-a337-c77844897fab` | ai | 0.717 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c66ffeb1-fd79-4d8f-965f-27e39d890def` | ai | 0.716 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `d0b817cf-a2f7-4b9b-8e70-86f5f3eec0de` | unsure | 0.402 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `677cec0c-5a04-47b3-8826-224e22d3f26b` | unsure | 0.406 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `d2c23bcb-bedf-4663-9a43-3c754801a0d2` | human | 0.270 | HELD |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `be091092-a268-4355-acb6-6843d4cedab4` | unsure | 0.568 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3b322649-91d2-4ad6-a0cd-969ddce85c5a` | unsure | 0.401 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4118b825-b743-4cde-a964-f85015b0a360` | unsure | 0.364 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `6b1d090d-07c5-4a0b-96bb-bbc65b7a340d` | unsure | 0.609 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `3ca6c1b9-d2ed-40e5-b834-ffc81f32d016` | human | 0.287 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `493c0a0a-b345-44f5-bdc4-d02792291c63` | human | 0.256 | HELD |
| MF05 | malformed | text is a very long single word | 200 | `914ebcf6-e4f0-4ded-8b5d-b516a3ec718e` | ai | 0.786 | HELD |
| MF06 | malformed | text is emoji only | 200 | `02765323-4aca-48b3-8804-5f71d339ca0a` | ai | 0.749 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `f8702d7b-3d83-40b1-87bd-18be170190e5` | ai | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `aab0f218-4807-476d-85f5-a7da9a36ba12` | unsure | 0.407 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `4ad2be7c-f6fb-4b31-aece-2229ad4be8e8` | human | 0.312 | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a3d549c9-57e5-4c32-807d-b241f9f636e8` | human | 0.302 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e6e3ceb1-c202-411c-a78e-09ee916fe3a4` | human | 0.302 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b90735a3-f3ec-48b1-b312-261a04947c0f` | human | 0.302 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dbf37f77-f675-4902-908e-fdd01ad6a0b4` | human | 0.302 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `46935585-f3ad-4262-9daf-f02a47a302ee` | human | 0.302 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `85d82d47-bdd4-4b94-9666-58761afc3f5e` | human | 0.302 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `65f1daf4-44f6-47cf-a5d7-52b235d850d4` | human | 0.302 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `588b5304-342a-45ed-a7ba-002a1c587902` | human | 0.302 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `eb7b00bd-083d-4361-b02a-ea7b05ddfc0a` | human | 0.302 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e33f49c4-d647-42b9-a889-b9d2a9df1cfa` | human | 0.302 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

### Summary By Family

| Family | Total | HELD | BROKE | Description |
|---|---|---|---|---|
| `evasion` | 10 | 2 | 8 | AI text perturbations (typos, sentence fragments, padding) successfully pushed scores down into `unsure` (7) or `human` (1). Only EV04 and EV10 remained flagged as `ai`. |
| `false_positive` | 8 | 2 | 6 | 6 of 8 genuine human passages (formal register, non-native English speaker, rubric essay, technical documentation, template imitation, deliberate repetition) scored above 0.65 and were wrongly accused of being AI. Only FP01 and FP08 avoided the AI label. |
| `prompt_injection` | 6 | 6 | 0 | Instructions to ignore the check or inject hostile labels had no effect on the heuristic detector pipeline or audit log. All 6 evaluated as standard text without hijacking. |
| `malformed` | 20 | 20 | 0 | All edge cases and invalid JSON payloads were either cleanly rejected with HTTP 400 or handled gracefully with 200 without a single 500 crash. |
| `flood_same_creator` | 12 | 12 | 0 | First 10 rapid submissions succeeded (200), and the 11th and 12th were blocked with HTTP 429 Too Many Requests by the 10/min rate limiter. |
| **Total** | **56** | **42** | **14** | **42 HELD, 14 BROKE (0 crashes/500s).** |

**Ten audit log entries from the run**

```json
[
  {
    "timestamp": "2026-11-11T19:39:33+00:00",
    "content_id": "3e484177-a020-46b1-80c6-b269af00fb1b",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.7787,
    "combined_score": 0.7919,
    "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:32+00:00",
    "content_id": "c48462d1-1fa7-4f1b-a7b8-ffc53201df5d",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.7387,
    "style_score": 0.8889,
    "combined_score": 0.8138,
    "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:33+00:00",
    "content_id": "2275aba4-95cf-4449-a2bd-d096fc186689",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.8572,
    "combined_score": 0.8288,
    "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:31+00:00",
    "content_id": "88112a26-1133-4d8b-b76c-7b2289c34a58",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.808,
    "combined_score": 0.4858,
    "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:31+00:00",
    "content_id": "3951be86-3d00-4154-8f6e-7437a618aa8a",
    "creator_id": "attacker_EV02",
    "guess": "unsure",
    "model_score": 0.5943,
    "style_score": 0.4231,
    "combined_score": 0.5087,
    "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:31+00:00",
    "content_id": "9da0839d-6939-47ed-bd1c-94931ff63135",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "model_score": 0.3212,
    "style_score": 0.329,
    "combined_score": 0.3251,
    "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:33+00:00",
    "content_id": "d2c23bcb-bedf-4663-9a43-3c754801a0d2",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.3346,
    "combined_score": 0.2695,
    "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-11T19:39:35+00:00",
    "creator_id": "attacker_MF08",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_long",
    "text_length": 57639
  },
  {
    "timestamp": "2026-11-11T19:39:35+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "invalid_json"
  },
  {
    "timestamp": "2026-11-11T19:39:36+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

**Attack `FP03` (`attacker_FP03`): a non-native English speaker writing carefully about their first month in a new country.**

- **The submission text:**
  > *"I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. I am still learning the words that people use in the office. Sometimes I do not understand the jokes. But I am happy that I came here and I think it was a good decision for my family."*
- **What our pipeline returned:**
  - `model_score = 0.8051` (low perplexity under GPT-2 because common, high-frequency words follow standard syntactic transitions)
  - `style_score = 0.7787` (uniform sentence lengths averaging 11–13 words with basic periods and commas)
  - `combined_score = 0.7919` (`guess = "ai"`, well above `AI_THRESHOLD = 0.65`)
  - `label`: *"This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID."*
- **Why this is the worst outcome:**
  This is an authentic, heartfelt reflection written by an immigrant or second-language English writer trying their best to express a major life transition in clear, simple language. Because their prose lacks obscure vocabulary or erratic punctuation, both detector signals independently misread clarity as machine automation. Falsely accusing an earnest human writer of passing off AI-generated text is insulting, demoralizing, and the exact asymmetric harm that breaks community trust.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1. False-positive cap on authentic human writing | ≤ 1 of 10 (`<= 10%`) | 0/10 (0%) | 0/10 (0%) | 0/10 (0%) | MET |
| 2. Mean score separation between AI and human text | ≥ 0.30 mean gap | 0.5704 | 0.5704 | 0.5704 | MET |
| 3. Complete three-label reachability across score range | 3 of 3 labels | 3/3 | 3/3 | 3/3 | MET |
| 4. Graceful rejection of bad/malformed inputs | 5 of 5 (`100% 400`, 0 crashes) | 5/5 | 5/5 | 5/5 | MET |
| 5. Deterministic appeal state transition and unknown-ID handling | 4 of 4 (`3 under_review, 1 404`) | 4/4 | 4/4 | 4/4 | MET |

**Real output from one trial**, pasted as text, naming the file and function that produced it:
- **File:** `run_eval.py`
- **Function:** `run_eval.py::main` (recorded in `results/run_2026-11-11_1300_before.md`)

```json
{
  "criterion_1_my_own_writing": [
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.4759,
      "model_score": 0.3819,
      "style_score": 0.5699,
      "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
      "sent": "I spent three hours yesterday trying to tune my acoustic guitar after "
    },
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.5714,
      "model_score": 0.7152,
      "style_score": 0.4276,
      "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
      "sent": "My grandmother taught me how to knead sourdough bread when I was ten y"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.3362,
      "model_score": 0.3416,
      "style_score": 0.3307,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "We started climbing Mount Si before sunrise on Saturday morning. The l"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.2226,
      "model_score": 0.184,
      "style_score": 0.2612,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "Restoring an old steel bicycle frame from the nineteen-eighties taught"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.3222,
      "model_score": 0.2423,
      "style_score": 0.4022,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "Writing a letter by hand feels completely different than typing an ema"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.2484,
      "model_score": 0.3002,
      "style_score": 0.1965,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "Every summer, our family drove ten hours north to camp beside a glacia"
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.3304,
      "model_score": 0.3143,
      "style_score": 0.3465,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "Moving out of my college apartment took three days longer than planned"
    },
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.4226,
      "model_score": 0.6051,
      "style_score": 0.2401,
      "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
      "sent": "We adopted an orange tabby cat named Marmalade from the county animal "
    },
    {
      "status": 200,
      "guess": "unsure",
      "confidence": 0.4726,
      "model_score": 0.4262,
      "style_score": 0.519,
      "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call.",
      "sent": "Waiting on the subway platform late on a Tuesday night is a strangely "
    },
    {
      "status": 200,
      "guess": "human",
      "confidence": 0.2128,
      "model_score": 0.0688,
      "style_score": 0.3569,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression.",
      "sent": "Debugging embedded C code on a custom microcontroller can drive you ma"
    }
  ],
  "criterion_2_score_separation_sample": {
    "mean_ai_score": 0.8388,
    "mean_human_score": 0.2684,
    "separation_gap": 0.5704,
    "ai_sample_1": {
      "status": 200,
      "guess": "ai",
      "confidence": 0.8442,
      "model_score": 0.8733,
      "style_score": 0.8152,
      "sent": "The implementation of the proposed framework requires careful consider"
    },
    "human_sample_1": {
      "status": 200,
      "guess": "human",
      "confidence": 0.2226,
      "model_score": 0.184,
      "style_score": 0.2612,
      "sent": "Restoring an old steel bicycle frame from the nineteen-eighties taught"
    }
  },
  "criterion_3_three_label_reachability": [
    {
      "guess": "human",
      "confidence": 0.2226,
      "label": "We're confident this text was written by a person, showing the natural variety and pacing of human expression."
    },
    {
      "guess": "unsure",
      "confidence": 0.4759,
      "label": "We can't tell whether this was written by a person or generated by an AI. The writing shows a mix of patterns, so we are not making an automated call."
    },
    {
      "guess": "ai",
      "confidence": 0.8442,
      "label": "This text shows strong patterns typical of AI-generated writing. If you wrote this yourself, you can submit an appeal using your content ID."
    }
  ],
  "criterion_4_graceful_rejection_of_bad_inputs": [
    {
      "status": 400,
      "guess": null,
      "sent": "(empty text)"
    },
    {
      "status": 400,
      "guess": null,
      "sent": "{\"creator_id\": \"eval_bad_missing\"}"
    },
    {
      "status": 400,
      "guess": null,
      "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
    },
    {
      "status": 400,
      "guess": null,
      "sent": "hi"
    },
    {
      "status": 400,
      "guess": null,
      "sent": "word word word word word word word word word word word word word word "
    }
  ],
  "criterion_5_appeal_path_state_transition": [
    {
      "status": 200,
      "content_id": "472795dc-8063-4ff9-84ac-d83af9920772",
      "guess": "under_review",
      "appeal_status": "under_review",
      "message": "Your appeal has been received and this submission is now under review.",
      "reasoning": "I wrote this reflection myself about my guitar."
    },
    {
      "status": 200,
      "content_id": "12cb6140-723d-4ee3-98d8-26ab65389a2e",
      "guess": "under_review",
      "appeal_status": "under_review",
      "message": "Your appeal has been received and this submission is now under review.",
      "reasoning": "This is a genuine personal childhood memory."
    },
    {
      "status": 200,
      "content_id": "93dd3500-4e92-43ed-a43d-3ccfc6cc85a7",
      "guess": "under_review",
      "appeal_status": "under_review",
      "message": "Your appeal has been received and this submission is now under review.",
      "reasoning": "Personal account of a Pacific Northwest hike."
    },
    {
      "status": 404,
      "guess": "not_found",
      "appeal_status": "not_found",
      "message": "No submission found with content_id '00000000-0000-0000-0000-000000000000'."
    }
  ]
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [x] Rate limiting on /submit, with your numbers justified
       [x] The pasted run of status codes showing 429
       [x] Audit log with all nine fields, recording rejections too
       [x] The attack set run IN FULL, every input with an outcome
       [x] Ten audit log entries pasted as text
       [x] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
