import os
import json
import random
from typing import Dict, Any, List


def pick_random_file(root: str, recursive: bool, extensions: tuple[str, ...]) -> str:
    candidates = []
    if recursive:
        for r, _, files in os.walk(root):
            for f in files:
                if f.lower().endswith(extensions):
                    candidates.append(os.path.join(r, f))
    else:
        for f in os.listdir(root):
            p = os.path.join(root, f)
            if os.path.isfile(p) and f.lower().endswith(extensions):
                candidates.append(p)

    if not candidates:
        raise FileNotFoundError(f"No matching files found in {root}")

    return random.choice(candidates)


def load_json_sidecar(asset_path: str) -> Dict[str, Any]:
    base = os.path.splitext(os.path.basename(asset_path))[0]
    json_path = os.path.join(os.path.dirname(asset_path), base + ".json")
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def closest(value, candidates):
    return min(candidates, key=lambda x: abs(x - value))


def apply_resolution(values, params, modifications_enabled):
    if "width" not in params or "height" not in params:
        w, h = random.choice(values)
        params.setdefault("width", w)
        params.setdefault("height", h)
        return
    if not modifications_enabled:
        return
    w, h = closest(
        (params["width"] / params["height"]), [(v[0] / v[1]) for v in values]
    )


def merge_value(key, values, params, modifications_enabled):
    if key not in params:
        return params.setdefault(key, random.choice(values))
    if not modifications_enabled:
        return params[key]
    current = params[key]
    if isinstance(current, (int, float)):
        nums = [v for v in values if isinstance(v, (int, float))]
        if nums:
            params[key] = closest(current, nums)
    elif isinstance(current, str):
        if current not in values:
            params[key] = random.choice(values)
    return params[key]


def merge_json_rules(
    json_data: Dict[str, Any],
    params: Dict[str, Any],
    pos: Dict[str, List[str]],
    neg: Dict[str, List[str]],
    modifications_enabled: bool,
):
    for key, value in json_data.items():
        # Nested dict (e.g. upscale)
        if isinstance(value, dict):
            params.setdefault(key, {})
            merge_json_rules(value, params[key], pos, neg, modifications_enabled)
            continue

        if not isinstance(value, list) or not value:
            continue

        if key == "resolution":
            apply_resolution(value, params, modifications_enabled)
            continue

        if key in ("positive_prompt", "positive_prompts"):
            pos.setdefault("json", []).extend(value)
            continue

        if key in ("negative_prompt", "negative_prompts"):
            neg.setdefault("json", []).extend(value)
            continue

        merge_value(key, value, params, modifications_enabled)
