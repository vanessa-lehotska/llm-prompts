"""Configuration loading and management"""
import json
import os
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json file"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    return {"modes": {}}


def get_mode_config(config: Dict[str, Any], mode: str) -> Dict[str, Any]:
    """Get configuration for a specific mode"""
    return config.get("modes", {}).get(mode, {})


def get_level_config(mode_config: Dict[str, Any], level: int) -> Dict[str, Any]:
    """Get configuration for a specific level within a mode"""
    levels = mode_config.get("levels", {})
    level_key = str(level)
    
    if level_key not in levels:
        raise ValueError(f"Invalid level: {level}")
    
    return levels[level_key]
