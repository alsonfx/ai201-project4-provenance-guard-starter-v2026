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
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `text` | `string` | Yes | The text submission to evaluate (must contain at least 3 tokens / a few sentences and not exceed maximum character limits). |
  | `creator_id` | `string` | No (defaults to `"anonymous"`) | Identifier for the submitting writer or account. |

- **Success Response (`200 OK`, `application/json`):**
  | Field | Type | Description |
  |---|---|---|
  | `content_id` | `string` | Unique identifier (`uuid4` hex/string) generated for this submission, used to look up or appeal the decision. |
  | `guess` | `string` | Machine-readable classification: `"human"`, `"unsure"`, or `"ai"`. |
  | `confidence` | `float` | Combined score in `[0.0, 1.0]` output by `scoring.combine_signals` (`0.0` = human, `1.0` = AI). |
  | `label` | `string` | Plain-English sentence shown to the reader/writer (from `scoring.score_to_label`). |
  | `model_score` | `float` | Signal 1 score in `[0.0, 1.0]` from `detector.model_signal`. |
  | `style_score` | `float` | Signal 2 score in `[0.0, 1.0]` from `stylometry.style_signal`. |
  | `status` | `string` | Initial lifecycle state: `"decided"`. |

- **Error Response (`400 Bad Request` / `429 Too Many Requests`, `application/json`):**
  Returns `{"error": "<reason_code>", "message": "<human-readable explanation>"}` and records a `"rejected"` entry in `logs/audit.jsonl`.

#### 2. `POST /appeal`
- **Request (`application/json`):**
  | Field | Type | Required | Description |
  |---|---|---|---|
  | `content_id` | `string` | Yes | The `content_id` returned by an earlier `POST /submit` call. |
  | `reasoning` | `string` | Yes | The writer's explanation contesting the classification. |

- **Success Response (`200 OK`, `application/json`):**
  | Field | Type | Description |
  |---|---|---|
  | `content_id` | `string` | The appealed submission's `content_id`. |
  | `creator_id` | `string` | The `creator_id` associated with the original submission. |
  | `status` | `string` | Updated lifecycle status: `"under_review"`. |
  | `reasoning` | `string` | Echo of the writer's submitted appeal reasoning. |
  | `message` | `string` | Confirmation message to the writer that their appeal has been logged. |

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

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
  "content_id": "084737ae-7047-44d2-8924-425fd12a9be0",
  "guess": "ai",
  "label": "PLACEHOLDER — Milestone 3 single-signal check.",
  "model_score": 0.8864,
  "status": "decided",
  "style_score": 0.8277
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "6b50c443-6f5c-4ce9-b5b1-ba532bd8d1be", "reasoning": "..."}'
```

```json

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
      "combined_score": 0.1658,
      "content_id": "1c94cd3a-a872-406a-8a41-8307adc7d4ed",
      "creator_id": "formal_human",
      "guess": "human",
      "label": "PLACEHOLDER — Milestone 3 single-signal check.",
      "model_score": 0.3278,
      "status": "decided",
      "style_score": 0.0039,
      "timestamp": "2026-11-04T23:31:54+00:00"
    },
    {
      "combined_score": 0.6869,
      "content_id": "375d44ef-5702-4a96-98b0-9bdcbf0898c0",
      "creator_id": "lightly_edited_ai",
      "guess": "ai",
      "label": "PLACEHOLDER — Milestone 3 single-signal check.",
      "model_score": 0.6456,
      "status": "decided",
      "style_score": 0.7282,
      "timestamp": "2026-11-04T23:31:54+00:00"
    },
    {
      "combined_score": 0.857,
      "content_id": "084737ae-7047-44d2-8924-425fd12a9be0",
      "creator_id": "test_ai",
      "guess": "ai",
      "label": "PLACEHOLDER — Milestone 3 single-signal check.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": 0.8277,
      "timestamp": "2026-11-04T23:33:06+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
