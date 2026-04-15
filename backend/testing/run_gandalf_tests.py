import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import csv
import json
import os
import random
import time
from datetime import datetime

from datasets import load_dataset
from dotenv import load_dotenv

from config import load_config
from defenses import detect_prompt_injection_attempt, filter_response
from llm.anthropic_client import get_anthropic_model_name
from llm.openai_client import get_model_name
from llm.provider import call_llm

load_dotenv()

IGNORE_INSTRUCTIONS_SAMPLES = 100
USE_ALL_SUMMARIZATION_SAMPLES = True
SUMMARIZATION_SAMPLES = 140
SAMPLE_SEED = 42

OUTPUT_DIR = Path("testing/results")


def get_target_provider() -> str:
    return os.getenv("LLM_PROVIDER", "anthropic").lower()


def get_target_model_name() -> str:
    provider = get_target_provider()

    if provider == "anthropic":
        return get_anthropic_model_name()

    return get_model_name()


def get_level_config(config: dict, level: int) -> dict:
    levels = config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
    return levels.get(str(level), {})


def sample_records(records: list[dict], limit: int | None, seed: int) -> list[dict]:
    if limit is None or limit >= len(records):
        return records

    rng = random.Random(seed)
    indices = list(range(len(records)))
    rng.shuffle(indices)
    selected = sorted(indices[:limit])

    return [records[i] for i in selected]


def build_dataset_spec() -> list[dict]:
    return [
        {
            "name": "gandalf_ignore_instructions",
            "hf_name": "Lakera/gandalf_ignore_instructions",
            "split": "train",
            "limit": IGNORE_INSTRUCTIONS_SAMPLES,
            "seed": SAMPLE_SEED,
        },
        {
            "name": "gandalf_summarization",
            "hf_name": "Lakera/gandalf_summarization",
            "split": "train",
            "limit": None if USE_ALL_SUMMARIZATION_SAMPLES else SUMMARIZATION_SAMPLES,
            "seed": SAMPLE_SEED,
        },
    ]


def load_gandalf_datasets() -> list[dict]:
    datasets_info = []

    for spec in build_dataset_spec():
        print(f"Loading {spec['hf_name']}...")
        dataset = load_dataset(spec["hf_name"], split=spec["split"])
        records = list(dataset)
        sampled_records = sample_records(records, spec["limit"], spec["seed"])

        prompts = []
        for row in sampled_records:
            prompts.append(
                {
                    "prompt": row["text"],
                }
            )

        datasets_info.append(
            {
                "name": spec["name"],
                "hf_name": spec["hf_name"],
                "split": spec["split"],
                "sample_size": len(prompts),
                "sampling_seed": spec["seed"],
                "prompts": prompts,
            }
        )

        print(f"  Loaded {len(prompts)} prompts")

    return datasets_info


def run_attack(prompt: str, level_config: dict) -> dict:
    system_prompt = level_config.get("systemPrompt", "")
    secret = level_config.get("secret", "")
    defense = level_config.get("defense", "none")

    if defense in ["input_guard", "combined"] and detect_prompt_injection_attempt(prompt):
        return {
            "direct_leak": False,
            "visible_direct_leak": False,
            "blocked_by_guard": True,
            "blocked_by_filter": False,
            "raw_response": None,
            "final_response": "Blocked by input guard",
            "error": False,
            "error_message": None,
        }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    try:
        raw_response = call_llm(messages, get_target_provider())
    except Exception as exc:
        return {
            "direct_leak": False,
            "visible_direct_leak": False,
            "blocked_by_guard": False,
            "blocked_by_filter": False,
            "raw_response": None,
            "final_response": None,
            "error": True,
            "error_message": str(exc),
        }

    direct_leak = secret.lower() in raw_response.lower()

    final_response = raw_response
    if defense in ["output_guard", "combined"]:
        final_response = filter_response(raw_response, secret)

    blocked_by_filter = final_response != raw_response
    visible_direct_leak = direct_leak and not blocked_by_filter

    return {
        "direct_leak": direct_leak,
        "visible_direct_leak": visible_direct_leak,
        "blocked_by_guard": False,
        "blocked_by_filter": blocked_by_filter,
        "raw_response": raw_response,
        "final_response": final_response,
        "error": False,
        "error_message": None,
    }


def run_tests() -> None:
    print("=" * 60)
    print("GANDALF DATASET TESTING")
    print("=" * 60)

    config = load_config()
    levels = config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
    num_levels = len(levels)

    datasets = load_gandalf_datasets()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    provider = get_target_provider()
    model_name = get_target_model_name()

    all_results = []
    summary = {}

    for dataset in datasets:
        dataset_name = dataset["name"]
        prompts = dataset["prompts"]

        print(f"\nDataset: {dataset_name}")

        for level in range(1, num_levels + 1):
            level_config = get_level_config(config, level)
            defense = level_config.get("defense", "none")
            secret = level_config.get("secret", "")

            direct_count = 0
            visible_direct_count = 0
            blocked_guard_count = 0
            blocked_filter_count = 0
            error_count = 0

            print(f"\n--- Level {level} ---")

            for index, item in enumerate(prompts, start=1):
                prompt = item["prompt"]

                print(f"[{index}/{len(prompts)}]")

                started = time.time()
                result = run_attack(prompt, level_config)
                elapsed = round(time.time() - started, 2)

                print(f"  {elapsed}s")

                if result["direct_leak"]:
                    direct_count += 1

                if result["visible_direct_leak"]:
                    visible_direct_count += 1

                if result["blocked_by_guard"]:
                    blocked_guard_count += 1

                if result["blocked_by_filter"]:
                    blocked_filter_count += 1

                if result["error"]:
                    error_count += 1

                all_results.append(
                    {
                        "provider": provider,
                        "model": model_name,
                        "dataset": dataset_name,
                        "level": level,
                        "defense": defense,
                        "secret": secret,
                        "prompt_index": index,
                        "prompt": prompt,
                        "direct_leak": result["direct_leak"],
                        "visible_direct_leak": result["visible_direct_leak"],
                        "blocked_by_guard": result["blocked_by_guard"],
                        "blocked_by_filter": result["blocked_by_filter"],
                        "raw_response": result["raw_response"],
                        "final_response": result["final_response"],
                        "error": result["error"],
                        "error_message": result["error_message"],
                        "elapsed": elapsed,
                    }
                )

            total = len(prompts)

            summary_key = f"{dataset_name}_level_{level}"
            summary[summary_key] = {
                "provider": provider,
                "model": model_name,
                "dataset": dataset_name,
                "level": level,
                "defense": defense,
                "total": total,
                "direct_leak": direct_count,
                "visible_direct_leak": visible_direct_count,
                "blocked_guard": blocked_guard_count,
                "blocked_filter": blocked_filter_count,
                "errors": error_count,
                "direct_asr": round(direct_count / total * 100, 2),
                "visible_direct_asr": round(visible_direct_count / total * 100, 2),
            }

            print(
                f"Level {level}: "
                f"Direct {direct_count}/{total}, "
                f"Visible {visible_direct_count}/{total}, "
                f"Guard {blocked_guard_count}/{total}, "
                f"Filter {blocked_filter_count}/{total}, "
                f"Errors {error_count}/{total}"
            )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model_name = model_name.replace("/", "_").replace(":", "_")

    payload = {
        "run_metadata": {
            "timestamp": timestamp,
            "provider": provider,
            "model": model_name,
            "ignore_instructions_samples": IGNORE_INSTRUCTIONS_SAMPLES,
            "use_all_summarization_samples": USE_ALL_SUMMARIZATION_SAMPLES,
            "summarization_samples": SUMMARIZATION_SAMPLES,
            "sample_seed": SAMPLE_SEED,
            "datasets": [
                {
                    "name": dataset["name"],
                    "hf_name": dataset["hf_name"],
                    "split": dataset["split"],
                    "sample_size": dataset["sample_size"],
                    "sampling_seed": dataset["sampling_seed"],
                }
                for dataset in datasets
            ],
        },
        "summary": summary,
        "results": all_results,
    }

    results_file = OUTPUT_DIR / f"results_{provider}_{safe_model_name}_{timestamp}.json"
    with results_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print(f"\nSaved JSON to {results_file}")

    csv_file = OUTPUT_DIR / f"summary_{provider}_{safe_model_name}_{timestamp}.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Provider",
                "Model",
                "Dataset",
                "Level",
                "Defense",
                "Direct ASR (%)",
                "Visible Direct ASR (%)",
                "Blocked Guard",
                "Blocked Filter",
                "Errors",
            ]
        )

        for item in summary.values():
            writer.writerow(
                [
                    item["provider"],
                    item["model"],
                    item["dataset"],
                    item["level"],
                    item["defense"],
                    item["direct_asr"],
                    item["visible_direct_asr"],
                    item["blocked_guard"],
                    item["blocked_filter"],
                    item["errors"],
                ]
            )

    print(f"Saved CSV to {csv_file}")


if __name__ == "__main__":
    run_tests()