# manage.py - Restart or solve the lab
import os
import shutil
import sys


lab_dir = os.path.dirname(os.path.abspath(__file__))
manage_dir = os.path.join(lab_dir, "_manage")


def copy_tree(source_dir):
    """Copy all files from source_dir to lab_dir, preserving subdirectory structure."""
    for root, dirs, files in os.walk(source_dir):
        rel_root = os.path.relpath(root, source_dir)
        for name in files:
            src = os.path.join(root, name)
            rel_path = os.path.join(rel_root, name) if rel_root != "." else name
            dest = os.path.join(lab_dir, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(src, dest)
            print(f"  Restored {rel_path}")


def restart():
    source = os.path.join(manage_dir, "starter")
    if not os.path.isdir(source):
        print("Error: _manage/starter/ not found.")
        raise SystemExit(1)

    # Restore starter files
    copy_tree(source)

    # Remove output directory
    output_dir = os.path.join(lab_dir, "output")
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
        print("  Deleted output/")

    # Remove generated files
    generated_files = [
        os.path.join("pr_files", "test_utils_new.py"),
    ]
    for filepath in generated_files:
        full_path = os.path.join(lab_dir, filepath)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"  Deleted {filepath}")

    print("\nRestart complete. Follow the README to start again.")


def solve():
    source = os.path.join(manage_dir, "solved")
    if not os.path.isdir(source):
        print("Error: _manage/solved/ not found.")
        raise SystemExit(1)
    copy_tree(source)
    print("\nAll solutions applied. Run 'python pipeline.py' to see the completed lab.")
    print("To restart with TODOs: python manage.py restart")


def usage():
    print("Usage: python manage.py <command>")
    print()
    print("Commands:")
    print("  restart  Restore starter files (TODOs intact)")
    print("  solve    Apply completed solutions")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("restart", "solve"):
        usage()
        raise SystemExit(1)

    command = sys.argv[1]
    if command == "restart":
        restart()
    elif command == "solve":
        solve()
