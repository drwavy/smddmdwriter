import os
import subprocess
from pathlib import Path

def get_valid_base_directory() -> Path:
    while True:
        base_directory = input("Enter the base directory: ").strip()
        if not base_directory:
            print("Directory cannot be blank. Please try again.")
            continue

        base_path = Path(base_directory)
        if base_path.is_dir():
            print(f"Base directory set to: {base_path}")
            return base_path
        else:
            print(f"'{base_directory}' is not a valid directory. Please try again.")

def run_script(script_name: str):
    try:
        print(f"Running {script_name}...")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")

def main():
    print("S      M     D    D        M   D    WRITER")
    print("Social Media Data Download MetaData WRITER")
    print("Metadata is not Meta's Data!")
    input("Press ENTER to begin...")

    base_directory = get_valid_base_directory()
    print(f"Working with base directory: {base_directory}")

    print("Select an option:")
    print("1. Instagram HTML")
    print("2. Instagram JSON")
    print("3. Snapchat Data")

    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "1":
        run_script("instagram_html_inbox.py")
        run_script("instagram_html_content.py")
    elif choice == "2":
        run_script("instagram_json_inbox.py")
        run_script("instagram_json_content.py")
        run_script("instagram_json_timestamp.py")
    elif choice == "3":
        run_script("snapchat.py")
    else:
        print("Invalid choice. Exiting.")
        return

    print("The CSV files have been generated. (Does not apply to Snapchat data, ignore all errors atp.")
    edit_choice = input("Press ENTER to continue or type 'edit' to open the folder: ").strip()
    if edit_choice.lower() == "edit":
        csv_folder = 'csv'
        if os.name == "nt":
            os.startfile(csv_folder)
        elif os.name == "posix":
            os.system(f"open {csv_folder}" if "darwin" in os.sys.platform else f"xdg-open {csv_folder}")

    input("Press ENTER to continue processing...")
    run_script("caption_flattener.py")
    run_script("file_repair.py")
    run_script("apply.py")

    print("Operations are completed. Press ENTER to exit or type a new directory to restart.")
    restart_choice = input("New directory (or press ENTER to exit): ").strip()
    if restart_choice:
        main()

if __name__ == "__main__":
    main()
