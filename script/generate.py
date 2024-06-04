import json
from pathlib import Path
import shutil
import os
from header import generate_prototypes
from test import generate_test_cases
from signals import generate_signal_func
from text import generate_signals_txt

ROOT = Path(__file__).parent

try:
    with open('../script/data.json', 'r') as f:
        data = json.load(f)

except FileNotFoundError:
    print("File not found. Please check the file path.")
except json.JSONDecodeError:
    print("Error decoding JSON. Please check if the file contains valid JSON.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

TEST_DIR = Path(ROOT.parent, 'test')
SIGNALS_DIR = Path(ROOT.parent, 'lib', 'signals')

try:
    shutil.rmtree(TEST_DIR, True)
    shutil.rmtree(SIGNALS_DIR, True)
    os.makedirs(TEST_DIR, exist_ok=True)
    os.makedirs(SIGNALS_DIR, exist_ok=True)

except:
    print("Error creating directories")
    exit(1)

generate_prototypes(data)
generate_test_cases(data)
generate_signal_func(data)
generate_signals_txt(data)
