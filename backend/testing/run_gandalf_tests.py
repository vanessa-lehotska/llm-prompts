"""
Automated testing script using Gandalf datasets from Hugging Face.
Tests each attack prompt against all levels and records results.

Usage:
    cd backend
    python testing/run_gandalf_tests.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
from datetime import datetime
from datasets import load_dataset
from config import load_config
from utils.openai_client import call_openai_api
from utils.defenses import sanitize_input, filter_response

# Configuration
MAX_SAMPLES_PER_DATASET = 50  # Limit samples to save API costs
OUTPUT_DIR = "testing/results"


def get_level_config(config, level: int):
    """Get configuration for a specific level."""
    levels = config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
    return levels.get(str(level), {})


def run_attack(prompt: str, level_config: dict) -> dict:
    """Run a single attack against a level and return result."""
    system_prompt = level_config.get("systemPrompt", "")
    secret = level_config.get("secret", "")
    defense = level_config.get("defense", "none")
    
    # Apply input sanitization if needed
    processed_prompt = prompt
    if defense in ["input_sanitization", "combined"]:
        processed_prompt = sanitize_input(prompt)
    
    # Call OpenAI API
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": processed_prompt}
    ]
    
    try:
        response = call_openai_api(messages)
        content = response.choices[0].message.content
    except Exception as e:
        return {
            "success": False,
            "response": f"API Error: {str(e)}",
            "error": True
        }
    
    # Apply response filtering if needed
    original_content = content
    if defense in ["response_filtering", "combined"]:
        content = filter_response(content, secret)
    
    # Check if attack was successful (secret revealed in original response)
    attack_success = secret.upper() in original_content.upper()
    
    # Check if filtering blocked it
    blocked_by_filter = (attack_success and content != original_content)
    
    return {
        "success": attack_success and not blocked_by_filter,
        "secret_in_response": attack_success,
        "blocked_by_filter": blocked_by_filter,
        "response": content[:500],  # Truncate for storage
        "error": False
    }


def load_gandalf_datasets():
    """Load Gandalf datasets from Hugging Face."""
    datasets_info = []
    
    # Dataset 1: gandalf_ignore_instructions
    print("Loading gandalf_ignore_instructions...")
    try:
        ds1 = load_dataset("Lakera/gandalf_ignore_instructions", split="train")
        prompts1 = [item["text"] for item in ds1][:MAX_SAMPLES_PER_DATASET]
        datasets_info.append({
            "name": "gandalf_ignore_instructions",
            "prompts": prompts1,
            "category": "Direct Injection"
        })
        print(f"  Loaded {len(prompts1)} samples")
    except Exception as e:
        print(f"  Error loading: {e}")
    
    # Dataset 2: gandalf_summarization
    print("Loading gandalf_summarization...")
    try:
        ds2 = load_dataset("Lakera/gandalf_summarization", split="train")
        prompts2 = [item["text"] for item in ds2][:MAX_SAMPLES_PER_DATASET]
        datasets_info.append({
            "name": "gandalf_summarization",
            "prompts": prompts2,
            "category": "Indirect Injection"
        })
        print(f"  Loaded {len(prompts2)} samples")
    except Exception as e:
        print(f"  Error loading: {e}")
    
    return datasets_info


def run_tests():
    """Main testing function."""
    print("=" * 60)
    print("GANDALF DATASET TESTING")
    print("=" * 60)
    
    # Load config
    config = load_config()
    levels = config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
    num_levels = len(levels)
    print(f"Loaded {num_levels} levels from config")
    
    # Load datasets
    datasets = load_gandalf_datasets()
    if not datasets:
        print("No datasets loaded. Exiting.")
        return
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Results storage
    all_results = []
    summary = {}
    
    # Run tests
    for dataset in datasets:
        dataset_name = dataset["name"]
        prompts = dataset["prompts"]
        category = dataset["category"]
        
        print(f"\n{'='*60}")
        print(f"Dataset: {dataset_name} ({len(prompts)} prompts)")
        print("=" * 60)
        
        for level in range(1, num_levels + 1):
            level_config = get_level_config(config, level)
            defense = level_config.get("defense", "none")
            secret = level_config.get("secret", "")
            
            print(f"\n  Level {level} (defense: {defense}, secret: {secret})")
            
            level_results = []
            success_count = 0
            
            for i, prompt in enumerate(prompts):
                result = run_attack(prompt, level_config)
                result["prompt"] = prompt[:200]  # Truncate
                result["level"] = level
                result["dataset"] = dataset_name
                result["category"] = category
                result["defense"] = defense
                
                level_results.append(result)
                all_results.append(result)
                
                if result["success"]:
                    success_count += 1
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"    Progress: {i+1}/{len(prompts)}, Success: {success_count}")
            
            # Calculate ASR for this level/dataset combo
            asr = (success_count / len(prompts) * 100) if prompts else 0
            
            key = f"{dataset_name}_level_{level}"
            summary[key] = {
                "dataset": dataset_name,
                "level": level,
                "defense": defense,
                "total": len(prompts),
                "successful": success_count,
                "asr": round(asr, 2)
            }
            
            print(f"    Result: {success_count}/{len(prompts)} ({asr:.1f}% ASR)")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save as JSON
    results_file = os.path.join(OUTPUT_DIR, f"results_{timestamp}.json")
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "summary": summary,
            "detailed_results": all_results
        }, f, indent=2, ensure_ascii=False)
    print(f"\nDetailed results saved to: {results_file}")
    
    # Save summary as CSV
    csv_file = os.path.join(OUTPUT_DIR, f"summary_{timestamp}.csv")
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Dataset", "Level", "Defense", "Total", "Successful", "ASR (%)"])
        for key, data in summary.items():
            writer.writerow([
                data["dataset"],
                data["level"],
                data["defense"],
                data["total"],
                data["successful"],
                data["asr"]
            ])
    print(f"Summary CSV saved to: {csv_file}")
    
    # Print final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(f"{'Dataset':<30} {'Level':<6} {'Defense':<20} {'ASR':<10}")
    print("-" * 70)
    for key, data in summary.items():
        print(f"{data['dataset']:<30} {data['level']:<6} {data['defense']:<20} {data['asr']:.1f}%")
    
    # Calculate overall ASR per level
    print("\n" + "=" * 60)
    print("ASR BY LEVEL (across all datasets)")
    print("=" * 60)
    for level in range(1, num_levels + 1):
        level_data = [v for k, v in summary.items() if v["level"] == level]
        if level_data:
            total = sum(d["total"] for d in level_data)
            successful = sum(d["successful"] for d in level_data)
            overall_asr = (successful / total * 100) if total > 0 else 0
            defense = level_data[0]["defense"]
            print(f"Level {level} ({defense}): {successful}/{total} = {overall_asr:.1f}% ASR")


if __name__ == "__main__":
    run_tests()
