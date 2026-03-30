# config.py - Lab constants
import os

# Paths
PR_FILES_DIR = "pr_files"
SCHEMA_PATH = "review_schema.json"
PROMPT_PATH = os.path.join("prompts", "review_prompt.txt")
INTEGRATION_PROMPT_PATH = os.path.join("prompts", "integration_prompt.txt")
OUTPUT_DIR = "output"

# Console colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
