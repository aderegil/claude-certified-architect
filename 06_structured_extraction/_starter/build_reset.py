# build_reset.py - Build reset.zip from _starter/ files
# Run from the lab directory: python _starter/build_reset.py
import os
import zipfile

lab_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
starter_dir = os.path.join(lab_dir, "_starter")

files = [
    "main.py",
    "schema.py",
]

zip_path = os.path.join(lab_dir, "reset.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in files:
        src = os.path.join(starter_dir, f)
        arc_name = f.replace(os.sep, "/")
        zf.write(src, arc_name)
        info = zf.getinfo(arc_name)
        print(f"  {arc_name} ({info.file_size} bytes)")

print(f"\n{zip_path} rebuilt from _starter/")
