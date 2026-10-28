# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False-positive cap on authentic human writing (False positives)

Across 10 paragraphs of original human writing (including plain, unadorned prose), at most **1 out of 10 (`<= 10%`)** is labelled `"ai"` (`high-confidence AI`, combined `confidence >= 0.65`) in every trial across all three trials.

**Why this target:**
On a writing platform, the cost of errors is sharply asymmetric: missing an AI-generated post or placing a borderline submission into `"unsure"` is a minor moderation friction, whereas falsely accusing a real human writer of submitting AI work damages their reputation and trust. Because our `gpt2` perplexity signal has a structural blind spot against plain, everyday prose (such as non-native English writers or concise technical writers), capping false positives at `<= 1 in 10` forces our combining weights and `AI_THRESHOLD` (`0.65`) to protect human writers unless both signals agree strongly.

---

## 2. Mean score separation between clearly-AI and clearly-human text (Score spread)

Across a benchmark set of 5 unedited, formulaic AI-generated paragraphs and 5 specific, varied human-written paragraphs, the mean combined `confidence` score of the clearly-AI set exceeds the mean combined `confidence` score of the clearly-human set by at least **`0.30` points (`mean_AI - mean_human >= 0.30`)** across all three trials.

**Why this target:**
Our three label bands span `0.00–0.35` (`high-confidence human`), `0.35–0.65` (`unsure`, a `0.30`-wide buffer), and `0.65–1.00` (`high-confidence AI`). Requiring at least a `0.30` gap between average AI and average human scores verifies that our two signals (`detector.model_signal` and `stylometry.style_signal`) actually pull unedited machine prose and natural human prose into their respective outer bands instead of clustering every submission around `0.50`.

---

## 3. Complete three-label reachability (Label coverage)

Across a calibration suite of 6 submissions spanning clearly human writing, borderline/lightly edited prose, and clearly AI-generated prose, **all 3 distinct `guess` values (`"human"`, `"unsure"`, and `"ai"`)—and all 3 corresponding reader-facing `label` strings—are produced at least once (`3 of 3 labels reached`)** in every trial.

**Why this target:**
A weighted average can only land between its inputs: if `style_signal` has a compressed range around `0.50` or if thresholds are set too close to `0.0` or `1.0`, one of the outer labels (`"human"` or `"ai"`) becomes mathematically unreachable in practice. Explicitly testing that all 3 labels are reached on every trial guarantees that none of our three user-facing label variants in `scoring.py::score_to_label` is dead code.

---

## 4. Graceful rejection and audit logging of malformed inputs (Bad input)

Across 5 malformed or adversarial `POST /submit` request bodies—(1) empty string `{"text": ""}`, (2) missing `"text"` field `{"creator_id": "test"}`, (3) null text `{"text": null}`, (4) sub-minimum 1-word text `{"text": "hello"}`, and (5) an oversized `50,000`-word payload—**5 out of 5 (`100%`) return HTTP `400 Bad Request` (with `0` HTTP `500` crashes) and record a `"status": "rejected"` entry in `logs/audit.jsonl`** across all three trials.

**Why this target:**
Under the hood, `detector.perplexity` raises `ValueError` on fewer than 3 tokens, `statistics.stdev` raises `StatisticsError` on fewer than 2 sentences, and huge payloads can stall CPU inference. Returning `400 Bad Request` and calling `audit.log_rejection` on 5/5 malformed inputs ensures the service never crashes with a `500` and never lets probing or malformed requests disappear silently from the audit log.

---

## 5. Deterministic appeal state transition and unknown-ID protection (The appeal path)

For 3 valid `content_id` values returned by `POST /submit`, calling `POST /appeal` with a non-empty `reasoning` string returns **HTTP `200 OK` with `"status": "under_review"` and appends an `"event": "appeal"` record to `logs/audit.jsonl` in 3 of 3 (`100%`) cases**, while calling `POST /appeal` with a non-existent `content_id` returns **HTTP `404 Not Found`** in 100% of cases.

**Why this target:**
When a human writer is caught by the false-positive blind spot traced in Milestone 1, `POST /appeal` is their only recourse. If the endpoint fails to verify `content_id` via `audit.entries_for(content_id)` or fails to append `"status": "under_review"` to `logs/audit.jsonl`, a typo or logging bug would silently discard a writer's appeal while telling them it succeeded.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
