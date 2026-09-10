import json
import os
class DataLoader:
    @staticmethod
    def load_json(relative_path):
        full_path = os.path.join(os.getcwd(), relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)