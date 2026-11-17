#!/usr/bin/env python3
"""
Capstone Evaluation & Cost Measurement Runner (Unit 9 — Shape C: POST /batch).

Usage:
    python run_capstone_eval.py --cost
    python run_capstone_eval.py --label before
    python run_capstone_eval.py --label after
"""

import argparse
import datetime as dt
import json
import sys
import time

import requests

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

DIVERSE_TEXTS = [
    "Restoring an old steel bicycle frame from the nineteen-eighties taught me patience. Every bolt had rusted shut, and WD-40 barely helped until I used a heat gun and an impact wrench to free the stuck bottom bracket without stripping the British threads.",
    "Debugging embedded C code on a custom microcontroller can drive you mad. The hardware timer was firing at half the expected clock frequency because an undocumented silicon revision had quietly altered the prescaler register bitfield in errata sheet four.",
    "I spent three hours yesterday trying to tune my acoustic guitar after replacing all six strings. The high E string snapped right as I reached standard pitch, so I had to bike down to the music shop in the rain to buy another single gauge string.",
    "My grandmother taught me how to knead sourdough bread when I was ten years old. She never used a kitchen scale; instead, she judged the dough by how sticky it felt against her palms and how quickly it sprang back after a firm poke with her thumb.",
    "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables. In conclusion, the results demonstrate that the approach is effective and scalable.",
]

WARM_3_ITEMS = [
    {"text": DIVERSE_TEXTS[0], "creator_id": "warm_item_1"},
    {"text": DIVERSE_TEXTS[2], "creator_id": "warm_item_2"},
    {"text": DIVERSE_TEXTS[4], "creator_id": "warm_item_3"},
]


def warm_up(url: str) -> None:
    """Ensure gpt2 is loaded in memory before timing/evaluating."""
    requests.post(
        f"{url}/submit",
        json={"text": DIVERSE_TEXTS[0], "creator_id": "cap_warmup"},
        timeout=90,
    )


def run_cost_measurement(url: str) -> None:
    """Measure 10 warm single runs and 10 warm 3-item batch runs."""
    warm_up(url)

    single_ms = []
    for i in range(10):
        t0 = time.perf_counter()
        resp = requests.post(
            f"{url}/submit",
            json={"text": DIVERSE_TEXTS[i % len(DIVERSE_TEXTS)], "creator_id": f"cost_s_{i}"},
            timeout=90,
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        data = resp.json()
        single_ms.append(data.get("duration_ms", elapsed_ms))

    batch_ms = []
    for i in range(10):
        resp = requests.post(
            f"{url}/batch",
            json={"items": WARM_3_ITEMS, "creator_id": f"cost_b_{i}"},
            timeout=90,
        )
        data = resp.json()
        batch_ms.append(data["duration_ms"])

    avg_s = sum(single_ms) / len(single_ms)
    avg_b = sum(batch_ms) / len(batch_ms)
    print(f"Single /submit (10 warm runs): avg={avg_s:.2f} ms ({avg_s/1000:.4f} s), "
          f"min={min(single_ms):.2f} ms, max={max(single_ms):.2f} ms")
    print(f"Batch  /batch 3-item (10 warm runs): avg={avg_b:.2f} ms ({avg_b/1000:.4f} s), "
          f"min={min(batch_ms):.2f} ms, max={max(batch_ms):.2f} ms")


def run_trial(url: str, trial_num: int) -> dict:
    """Execute all 5 Capstone criteria for one trial."""
    # Criterion 1: Batch decision parity (5 texts)
    c1_matches = 0
    c1_details = []
    single_results = []
    for idx, text in enumerate(DIVERSE_TEXTS):
        r = requests.post(
            f"{url}/submit",
            json={"text": text, "creator_id": f"c1_s_t{trial_num}_{idx}"},
            timeout=90,
        ).json()
        single_results.append(r)

    batch_r = requests.post(
        f"{url}/batch",
        json={
            "creator_id": f"c1_b_t{trial_num}",
            "items": [{"text": t, "creator_id": f"c1_bi_t{trial_num}_{i}"} for i, t in enumerate(DIVERSE_TEXTS)],
        },
        timeout=90,
    ).json()

    for idx, (s_res, b_res) in enumerate(zip(single_results, batch_r["results"])):
        same_guess = s_res["guess"] == b_res["guess"]
        close_conf = abs(s_res["confidence"] - b_res["confidence"]) <= 0.0001
        if same_guess and close_conf:
            c1_matches += 1
        c1_details.append({
            "index": idx,
            "single_guess": s_res["guess"],
            "batch_guess": b_res["guess"],
            "single_confidence": s_res["confidence"],
            "batch_confidence": b_res["confidence"],
            "match": same_guess and close_conf,
        })

    # Criterion 2: Partial-failure isolation (3 mixed batches)
    c2_passed = 0
    c2_details = []
    for idx in range(3):
        resp = requests.post(
            f"{url}/batch",
            json={
                "creator_id": f"c2_t{trial_num}_{idx}",
                "items": [
                    {"text": DIVERSE_TEXTS[0], "creator_id": f"c2_g1_{idx}"},
                    {"text": "", "creator_id": f"c2_b1_{idx}"},
                    {"text": DIVERSE_TEXTS[4], "creator_id": f"c2_g2_{idx}"},
                    {"creator_id": f"c2_b2_{idx}"},
                ],
            },
            timeout=90,
        )
        data = resp.json()
        ok = (
            resp.status_code == 200
            and data.get("succeeded") == 2
            and data.get("rejected") == 2
            and bool(data["results"][0].get("content_id"))
            and bool(data["results"][2].get("content_id"))
        )
        if ok:
            c2_passed += 1
        c2_details.append({
            "status": resp.status_code,
            "succeeded": data.get("succeeded"),
            "rejected": data.get("rejected"),
            "counts": data.get("counts"),
            "duration_ms": data.get("duration_ms"),
        })

    # Criterion 3: Batch size bound & malformed batch rejection (4 invalid bodies)
    c3_bodies = [
        {"items": [], "creator_id": f"c3_empty_t{trial_num}"},
        {"items": [{"text": DIVERSE_TEXTS[0], "creator_id": f"c3_11_{i}"} for i in range(11)],
         "creator_id": f"c3_oversize_t{trial_num}"},
        {"creator_id": f"c3_missing_t{trial_num}"},
        {"items": "hello", "creator_id": f"c3_nonlist_t{trial_num}"},
    ]
    c3_passed = 0
    c3_details = []
    before_count = requests.get(f"{url}/log", timeout=10).json()["count"]
    for body in c3_bodies:
        resp = requests.post(f"{url}/batch", json=body, timeout=30)
        data = resp.json()
        c3_details.append({"status": resp.status_code, "error": data.get("error"), "message": data.get("message")})
    after_logs = requests.get(f"{url}/log", timeout=10).json()["entries"][before_count:]
    rejected_logs = [e for e in after_logs if e.get("status") == "rejected"]
    if all(d["status"] == 400 for d in c3_details) and len(rejected_logs) == 4:
        c3_passed = 4

    # Criterion 4: End-to-end structured instrumentation completeness (5 /submit + 2 /batch)
    before_c4 = requests.get(f"{url}/log", timeout=10).json()["count"]
    for idx in range(4):
        requests.post(f"{url}/submit", json={"text": DIVERSE_TEXTS[idx], "creator_id": f"c4_s_t{trial_num}_{idx}"}, timeout=90)
    requests.post(f"{url}/submit", json={"text": "", "creator_id": f"c4_sbad_t{trial_num}"}, timeout=30)
    requests.post(
        f"{url}/batch",
        json={"creator_id": f"c4_b1_t{trial_num}", "items": [{"text": DIVERSE_TEXTS[0], "creator_id": f"c4_bi1_{trial_num}"}, {"text": DIVERSE_TEXTS[4], "creator_id": f"c4_bi2_{trial_num}"}]},
        timeout=90,
    )
    requests.post(f"{url}/batch", json={"items": [], "creator_id": f"c4_b2_t{trial_num}"}, timeout=30)

    c4_logs = requests.get(f"{url}/log", timeout=10).json()["entries"][before_c4:]
    c4_valid_fields = sum(
        1 for e in c4_logs
        if isinstance(e.get("timestamp"), str)
        and isinstance(e.get("status"), str)
        and isinstance(e.get("duration_ms"), (int, float))
        and e["duration_ms"] > 0
    )
    batch_summaries = [e for e in c4_logs if e.get("event") == "batch_summary"]
    c4_summary_ok = len(batch_summaries) == 1 and batch_summaries[0]["total_items"] == (
        batch_summaries[0]["succeeded"] + batch_summaries[0]["rejected"]
    )
    c4_pct = round(100.0 * c4_valid_fields / len(c4_logs), 1) if c4_logs else 0.0

    # Criterion 5: Warm batch latency ceiling (5 x 3-item batches < 3000 ms)
    c5_under = 0
    c5_latencies = []
    for idx in range(5):
        resp = requests.post(
            f"{url}/batch",
            json={"creator_id": f"c5_t{trial_num}_{idx}", "items": WARM_3_ITEMS},
            timeout=90,
        ).json()
        ms = resp["duration_ms"]
        c5_latencies.append(ms)
        if ms < 3000:
            c5_under += 1

    return {
        "c1": {"score": f"{c1_matches}/5", "met": c1_matches == 5, "details": c1_details},
        "c2": {"score": f"{c2_passed}/3", "met": c2_passed == 3, "details": c2_details},
        "c3": {"score": f"{c3_passed}/4", "met": c3_passed == 4, "details": c3_details},
        "c4": {"score": f"{c4_valid_fields}/{len(c4_logs)} ({c4_pct}%)", "met": c4_valid_fields == len(c4_logs) and c4_summary_ok, "sample_log": c4_logs[-2:]},
        "c5": {"score": f"{c5_under}/5", "met": c5_under >= 4, "latencies_ms": c5_latencies},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--cost", action="store_true")
    parser.add_argument("--label", default="before")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:
        print(f"Service not reachable at {args.url}", file=sys.stderr)
        sys.exit(1)

    if args.cost:
        run_cost_measurement(args.url)
        return

    warm_up(args.url)
    trials = [run_trial(args.url, t) for t in range(1, args.trials + 1)]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    out_path = config.RESULTS_DIR / f"capstone_run_{stamp}_{args.label}.md"

    def verdict(key: str) -> str:
        return "MET" if all(tr[key]["met"] for tr in trials) else "MISSED"

    lines = [
        f"# Capstone Run Log — {args.label}",
        "",
        f"- Produced by: `run_capstone_eval.py::main`",
        f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
        "|---|---|---|---|---|---|",
        f"| 1. Batch decision parity with `/submit` | 5 of 5 | {trials[0]['c1']['score']} | {trials[1]['c1']['score']} | {trials[2]['c1']['score']} | {verdict('c1')} |",
        f"| 2. Partial-failure isolation in mixed batches | 3 of 3 | {trials[0]['c2']['score']} | {trials[1]['c2']['score']} | {trials[2]['c2']['score']} | {verdict('c2')} |",
        f"| 3. Batch size bound & malformed batch rejection | 4 of 4 | {trials[0]['c3']['score']} | {trials[1]['c3']['score']} | {trials[2]['c3']['score']} | {verdict('c3')} |",
        f"| 4. End-to-end structured instrumentation completeness | 100% | {trials[0]['c4']['score']} | {trials[1]['c4']['score']} | {trials[2]['c4']['score']} | {verdict('c4')} |",
        f"| 5. Warm batch latency ceiling (`< 3000 ms`) | >= 4 of 5 | {trials[0]['c5']['score']} | {trials[1]['c5']['score']} | {trials[2]['c5']['score']} | {verdict('c5')} |",
        "",
        "## Real Output (Trial 1)",
        "",
        "```json",
        json.dumps(trials[0], indent=2),
        "```",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path.relative_to(config.ROOT)}")
    for line in lines[6:13]:
        print(line)


if __name__ == "__main__":
    main()
