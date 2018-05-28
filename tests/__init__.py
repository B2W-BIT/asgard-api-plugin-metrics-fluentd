import os
from typing import Dict

CURRENT_DIR = os.path.dirname(__file__)

def get_fixture(file_name: str) -> Dict:
    with open(os.path.join(CURRENT_DIR, file_name)) as fp:
        return json.load(fp)
