# reset.py - Reset lab to starter state
import os
import zipfile


def main():
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    starter_zip = os.path.join(lab_dir, "reset.zip")

    # Restore starter files from reset.zip
    if os.path.exists(starter_zip):
        with zipfile.ZipFile(starter_zip, "r") as z:
            z.extractall(lab_dir)
            restored = z.namelist()
        for name in restored:
            print(f"Restored {name}")
    else:
        print("Warning: reset.zip not found — cannot restore starter files.")

    # Remove scratch.md if it exists
    scratch_path = os.path.join(lab_dir, "scratch.md")
    if os.path.exists(scratch_path):
        os.remove(scratch_path)
        print("Deleted scratch.md")

    print("\nReset complete. Follow the README to start again.")


if __name__ == "__main__":
    main()
