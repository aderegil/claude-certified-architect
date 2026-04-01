# reset.py - Restore starter files from reset.zip
import os
import zipfile

lab_dir = os.path.dirname(os.path.abspath(__file__))
zip_path = os.path.join(lab_dir, "reset.zip")

if not os.path.exists(zip_path):
    print("reset.zip not found.")
    raise SystemExit(1)

with zipfile.ZipFile(zip_path, "r") as zf:
    for name in zf.namelist():
        dest = os.path.join(lab_dir, name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(zf.read(name))
        print(f"  restored {name}")

print("\nReset complete. Follow the README to start again.")
