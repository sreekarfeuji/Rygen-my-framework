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
        resolved = DataLoader._resolve_dates(data)
        logger.info("Dataset loaded: %s", full_path.name)
        return resolved
    @staticmethod
    def _resolve_dates(obj):
        if isinstance(obj, dict):
            return {k: DataLoader._resolve_dates(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [DataLoader._resolve_dates(item) for item in obj]
        if isinstance(obj, str):
            match = re.match(r"TODAY([+-]\d+)\s+(.*)", obj, re.IGNORECASE)
            if match:
                offset = int(match.group(1))
                resolved_date = (datetime.today() + timedelta(days=offset)).strftime("%m/%d/%Y")
                return f"{resolved_date} {match.group(2)}"
        return obj
