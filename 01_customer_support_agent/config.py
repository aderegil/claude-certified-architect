# config.py - Lab constants and policy values

MODEL = "claude-sonnet-4-20250514"
MAX_REFUND_AMOUNT = 500
MAX_LOOP_ITERATIONS = 10
ESCALATION_REASONS = ["fraud", "policy_gap", "customer_request", "repeated_failure"]

# Console colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"
