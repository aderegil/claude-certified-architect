# reset.py - Reset lab to starter state
import os
import shutil
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

    # Remove output directory
    output_dir = os.path.join(lab_dir, "output")
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
        print("Deleted output/")

    # Remove generated files
    generated_files = [
        os.path.join("pr_files", "test_utils_new.py"),
    ]
    for filepath in generated_files:
        full_path = os.path.join(lab_dir, filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Deleted {filepath}")

    print("\nReset complete. Follow the README to start again.")


if __name__ == "__main__":
    main()
