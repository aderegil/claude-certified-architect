# reset.py - Restore starter state for Lab 03

import os
import zipfile

STARTER_ZIP = ".starter.zip"
LAB_DIR = os.path.dirname(os.path.abspath(__file__))

# Files that get modified during the lab and need restoration
STARTER_FILES = ["main.py", "agents.py", "config.py"]


def reset():
    zip_path = os.path.join(LAB_DIR, STARTER_ZIP)

    if not os.path.exists(zip_path):
        print(f"No {STARTER_ZIP} found — nothing to reset.")
        return

    with zipfile.ZipFile(zip_path, "r") as zf:
        for filename in STARTER_FILES:
            if filename in zf.namelist():
                zf.extract(filename, LAB_DIR)
                print(f"  Restored {filename}")
            else:
                print(f"  Skipped {filename} (not in zip)")

    print("\nLab reset to starter state. Run 'python main.py' to start again.")


if __name__ == "__main__":
    reset()
