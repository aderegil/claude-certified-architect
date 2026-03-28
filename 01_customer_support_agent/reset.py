# reset.py - Reset lab to starter state
import os
import zipfile


def main():
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    starter_zip = os.path.join(lab_dir, ".starter.zip")
    env_file = os.path.join(lab_dir, ".env")

    # Restore starter files from .starter.zip
    if os.path.exists(starter_zip):
        with zipfile.ZipFile(starter_zip, "r") as z:
            z.extractall(lab_dir)
            restored = z.namelist()
        for name in restored:
            print(f"Restored {name}")
    else:
        print("Warning: .starter.zip not found — cannot restore starter files.")

    # Remove .env if it exists (student recreates from .env.example)
    if os.path.exists(env_file):
        os.remove(env_file)
        print("Deleted .env")

    print("\nReset complete. Follow the README to start again.")


if __name__ == "__main__":
    main()
