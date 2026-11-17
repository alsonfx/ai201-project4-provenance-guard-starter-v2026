#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import time
import uuid

from flask import Flask, g, jsonify, request

import audit
import config

app = Flask(__name__)


@app.before_request
def _record_request_start():
    g.start_time = time.perf_counter()


def _elapsed_ms(start_time: float | None = None) -> float:
    """Return elapsed wall-clock milliseconds with 4-decimal microsecond precision."""
    t0 = start_time if start_time is not None else getattr(g, "start_time", time.perf_counter())
    return max(round((time.perf_counter() - t0) * 1000, 4), 0.0001)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector
    import scoring
    import stylometry

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """
    body, status_code = _evaluate_submission(request.get_json(silent=True), start_time=None)
    return jsonify(body), status_code


def _evaluate_submission(
    payload,
    batch_id: str | None = None,
    start_time: float | None = None,
) -> tuple[dict, int]:
    """Validate, score, and audit-log one submission payload."""
    import detector
    import scoring
    import stylometry

    t0 = start_time
    extra_ctx = {"batch_id": batch_id} if batch_id else {}

    if not isinstance(payload, dict):
        duration_ms = _elapsed_ms(t0)
        audit.log_rejection(
            creator_id="unknown",
            reason="invalid_json",
            duration_ms=duration_ms,
            **extra_ctx,
        )
        return {
            "error": "invalid_input",
            "message": "Request body must be a JSON object.",
            "duration_ms": duration_ms,
        }, 400

    raw_creator = payload.get("creator_id")
    creator_id = (
        raw_creator.strip()
        if isinstance(raw_creator, str) and raw_creator.strip()
        else "anonymous"
    )

    raw_text = payload.get("text")
    if not isinstance(raw_text, str) or not raw_text.strip():
        duration_ms = _elapsed_ms(t0)
        audit.log_rejection(
            creator_id=creator_id,
            reason="missing_or_empty_text",
            duration_ms=duration_ms,
            **extra_ctx,
        )
        return {
            "error": "invalid_input",
            "message": "Field 'text' is required and must be a non-empty string.",
            "duration_ms": duration_ms,
        }, 400

    clean_text = raw_text.strip()
    if len(clean_text) > 20000:
        duration_ms = _elapsed_ms(t0)
        audit.log_rejection(
            creator_id=creator_id,
            reason="text_too_long",
            text_length=len(clean_text),
            duration_ms=duration_ms,
            **extra_ctx,
        )
        return {
            "error": "invalid_input",
            "message": "Field 'text' exceeds maximum length of 20,000 characters.",
            "duration_ms": duration_ms,
        }, 400

    try:
        m_score = detector.model_signal(clean_text)
    except ValueError as exc:
        duration_ms = _elapsed_ms(t0)
        audit.log_rejection(
            creator_id=creator_id,
            reason="text_too_short",
            text_length=len(clean_text),
            duration_ms=duration_ms,
            **extra_ctx,
        )
        return {
            "error": "invalid_input",
            "message": str(exc),
            "duration_ms": duration_ms,
        }, 400

    s_score = stylometry.style_signal(clean_text)
    confidence = scoring.combine_signals(m_score, s_score)
    guess, label = scoring.score_to_label(confidence)
    content_id = str(uuid.uuid4())
    duration_ms = _elapsed_ms(t0)

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=m_score,
        style_score=s_score,
        combined_score=confidence,
        label=label,
        status="decided",
        text_length=len(clean_text),
        duration_ms=duration_ms,
        **extra_ctx,
    )

    return {
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": m_score,
        "style_score": s_score,
        "status": "decided",
        "duration_ms": duration_ms,
    }, 200


@app.post("/batch")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def batch_submit():
    """
    Evaluate a bounded batch of submissions in one request (Capstone — Shape C).

    Expects JSON:
        {"items": [{"text": "...", "creator_id": "..."}, ...], "creator_id": "..."}
    """
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        duration_ms = _elapsed_ms()
        audit.log_rejection(
            creator_id="unknown",
            reason="invalid_batch_json",
            duration_ms=duration_ms,
        )
        return jsonify({
            "error": "invalid_input",
            "message": "Request body must be a JSON object.",
            "duration_ms": duration_ms,
        }), 400

    raw_creator = payload.get("creator_id")
    batch_creator = (
        raw_creator.strip()
        if isinstance(raw_creator, str) and raw_creator.strip()
        else "anonymous"
    )

    items = payload.get("items")
    if not isinstance(items, list) or len(items) == 0:
        duration_ms = _elapsed_ms()
        audit.log_rejection(
            creator_id=batch_creator,
            reason="missing_or_empty_batch_items",
            duration_ms=duration_ms,
        )
        return jsonify({
            "error": "invalid_input",
            "message": "Field 'items' is required and must be a non-empty list.",
            "duration_ms": duration_ms,
        }), 400

    if len(items) > config.BATCH_MAX_ITEMS:
        duration_ms = _elapsed_ms()
        audit.log_rejection(
            creator_id=batch_creator,
            reason="batch_too_large",
            batch_size=len(items),
            max_items=config.BATCH_MAX_ITEMS,
            duration_ms=duration_ms,
        )
        return jsonify({
            "error": "invalid_input",
            "message": f"Batch size {len(items)} exceeds maximum of {config.BATCH_MAX_ITEMS} items.",
            "duration_ms": duration_ms,
        }), 400

    batch_id = str(uuid.uuid4())
    results = []
    counts = {"human": 0, "unsure": 0, "ai": 0}
    succeeded = 0
    rejected = 0

    for idx, item in enumerate(items):
        item_t0 = time.perf_counter()
        item_body, item_status = _evaluate_submission(item, batch_id=batch_id, start_time=item_t0)
        item_entry = {"index": idx, "status": item_status, **item_body}
        results.append(item_entry)
        if item_status == 200:
            succeeded += 1
            counts[item_body["guess"]] += 1
        else:
            rejected += 1

    duration_ms = _elapsed_ms()
    audit.log_batch(
        batch_id=batch_id,
        creator_id=batch_creator,
        total_items=len(items),
        succeeded=succeeded,
        rejected=rejected,
        counts=counts,
        duration_ms=duration_ms,
    )

    return jsonify({
        "batch_id": batch_id,
        "total": len(items),
        "succeeded": succeeded,
        "rejected": rejected,
        "counts": counts,
        "duration_ms": duration_ms,
        "results": results,
    }), 200


@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. (Milestone 5)

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    1. Checks the content_id actually exists using audit.entries_for(content_id).
    2. Records the appeal with audit.log_appeal(...), moving status to under_review.
    3. Confirms to the writer.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_input",
            "message": "Request body must be a JSON object.",
        }), 400

    raw_content_id = payload.get("content_id")
    if not isinstance(raw_content_id, str) or not raw_content_id.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "Field 'content_id' is required and must be a non-empty string.",
        }), 400

    raw_reasoning = payload.get("reasoning")
    if not isinstance(raw_reasoning, str) or not raw_reasoning.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "Field 'reasoning' is required and must be a non-empty string.",
        }), 400

    content_id = raw_content_id.strip()
    reasoning = raw_reasoning.strip()

    entries = audit.entries_for(content_id)
    if not entries:
        return jsonify({
            "error": "not_found",
            "message": f"No submission found with content_id '{content_id}'.",
        }), 404

    creator_id = entries[0].get("creator_id", "anonymous")
    audit.log_appeal(content_id=content_id, creator_id=creator_id, reasoning=reasoning)

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "status": "under_review",
        "reasoning": reasoning,
        "message": "Your appeal has been received and this submission is now under review.",
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
