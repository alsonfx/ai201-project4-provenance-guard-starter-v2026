# Capstone Run Log — after

- Produced by: `run_capstone_eval.py::main`
- 3 trials · 2026-11-17 16:47

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Batch decision parity with `/submit` | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Partial-failure isolation in mixed batches | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 3. Batch size bound & malformed batch rejection | 4 of 4 | 4/4 | 4/4 | 4/4 | MET |
| 4. End-to-end structured instrumentation completeness | 100% | 9/9 (100.0%) | 9/9 (100.0%) | 9/9 (100.0%) | MET |
| 5. Warm batch latency ceiling (`< 3000 ms`) | >= 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

## Real Output (Trial 1)

```json
{
  "c1": {
    "score": "5/5",
    "met": true,
    "details": [
      {
        "index": 0,
        "single_guess": "human",
        "batch_guess": "human",
        "single_confidence": 0.2226,
        "batch_confidence": 0.2226,
        "match": true
      },
      {
        "index": 1,
        "single_guess": "human",
        "batch_guess": "human",
        "single_confidence": 0.2128,
        "batch_confidence": 0.2128,
        "match": true
      },
      {
        "index": 2,
        "single_guess": "unsure",
        "batch_guess": "unsure",
        "single_confidence": 0.4759,
        "batch_confidence": 0.4759,
        "match": true
      },
      {
        "index": 3,
        "single_guess": "unsure",
        "batch_guess": "unsure",
        "single_confidence": 0.5714,
        "batch_confidence": 0.5714,
        "match": true
      },
      {
        "index": 4,
        "single_guess": "ai",
        "batch_guess": "ai",
        "single_confidence": 0.8442,
        "batch_confidence": 0.8442,
        "match": true
      }
    ]
  },
  "c2": {
    "score": "3/3",
    "met": true,
    "details": [
      {
        "status": 200,
        "succeeded": 2,
        "rejected": 2,
        "counts": {
          "ai": 1,
          "human": 1,
          "unsure": 0
        },
        "duration_ms": 247.9398
      },
      {
        "status": 200,
        "succeeded": 2,
        "rejected": 2,
        "counts": {
          "ai": 1,
          "human": 1,
          "unsure": 0
        },
        "duration_ms": 199.9626
      },
      {
        "status": 200,
        "succeeded": 2,
        "rejected": 2,
        "counts": {
          "ai": 1,
          "human": 1,
          "unsure": 0
        },
        "duration_ms": 180.9731
      }
    ]
  },
  "c3": {
    "score": "4/4",
    "met": true,
    "details": [
      {
        "status": 400,
        "error": "invalid_input",
        "message": "Field 'items' is required and must be a non-empty list."
      },
      {
        "status": 400,
        "error": "invalid_input",
        "message": "Batch size 11 exceeds maximum of 10 items."
      },
      {
        "status": 400,
        "error": "invalid_input",
        "message": "Field 'items' is required and must be a non-empty list."
      },
      {
        "status": 400,
        "error": "invalid_input",
        "message": "Field 'items' is required and must be a non-empty list."
      }
    ]
  },
  "c4": {
    "score": "9/9 (100.0%)",
    "met": true,
    "sample_log": [
      {
        "batch_id": "4570c63c-8b09-41d6-b6cb-52f857dc8bf0",
        "counts": {
          "ai": 1,
          "human": 1,
          "unsure": 0
        },
        "creator_id": "c4_b1_t1",
        "duration_ms": 259.4682,
        "event": "batch_summary",
        "rejected": 0,
        "status": "completed",
        "succeeded": 2,
        "timestamp": "2026-11-17T23:47:37+00:00",
        "total_items": 2
      },
      {
        "creator_id": "c4_b2_t1",
        "duration_ms": 0.7267,
        "event": "rejected",
        "reason": "missing_or_empty_batch_items",
        "status": "rejected",
        "timestamp": "2026-11-17T23:47:37+00:00"
      }
    ]
  },
  "c5": {
    "score": "5/5",
    "met": true,
    "latencies_ms": [
      267.654,
      343.3149,
      282.2234,
      275.2176,
      344.2177
    ]
  }
}
```