import logging
import json
from pathlib import Path
import re
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class DataLoader:

    @staticmethod
    def load_json(relative_path):
        full_path = Path(__file__).resolve().parents[1] / relative_path
        logger.debug("Loading dataset file: %s", full_path.name)
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        resolved = DataLoader._resolve(data)
        logger.info("Dataset loaded: %s", full_path.name)
        return resolved

    @staticmethod
    def _resolve(obj):
        """Recursively resolve dynamic placeholders in JSON values."""
        if isinstance(obj, dict):
            return {k: DataLoader._resolve_value(k, v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [DataLoader._resolve(item) for item in obj]
        return obj

    @staticmethod
    def _resolve_value(key, value):
        if isinstance(value, (dict, list)):
            return DataLoader._resolve(value)
        if not isinstance(value, str) or value == "":
            return value

        # Resolve Location_Code: append a unique timestamp suffix
        if key == "Location_Code":
            suffix = datetime.now().strftime("%H%M%S")
            return f"{value}_{suffix}"

        # Resolve date markers: e.g. "TODAY+5 08:00 am" → "09/15/2026 08:00 am"
        match = re.match(r"TODAY([+-]\d+)\s+(.*)", value, re.IGNORECASE)
        if match:
            offset = int(match.group(1))
            time_part = match.group(2)
            resolved_date = (datetime.today() + timedelta(days=offset)).strftime("%m/%d/%Y")
            return f"{resolved_date} {time_part}"

        return value