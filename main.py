from pathlib import Path
import logging
import subprocess
from typing import Optional


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

# def get_valid_base_directory() -> Path:
#     while True:
#         base_directory = input("Enter the base directory: ").strip()
#         base_path = Path(base_directory)
#         if base_path.is_dir():
#             with open("base_directory.txt", "w", encoding="utf-8") as file:
#                 file.write(str(base_path))
#             logging.info(f"Base directory saved to base_directory.txt: {base_path}")
#             return base_path
#         else:
#             print(f"'{base_directory}' is not a valid directory. Please try again.")
import logging
from pathlib import Path


def get_valid_base_directory() -> Path:
    while True:
        base_directory = input("Enter the base directory: ").strip()
        if not base_directory:
            print("Directory cannot be blank. Please try again.")
            continue

        base_path = Path(base_directory)
        if base_path.is_dir():
            try:
                with open("base_directory.txt", "w", encoding="utf-8") as file:
                    file.write(str(base_path))
                logging.info(f"Base directory saved to base_directory.txt: {base_path}")
                return base_path
            except OSError as e:
                logging.error(f"Error saving the directory: {e}")
                print("An error occurred while saving the directory. Please try again.")
        else:
            logging.warning(f"Invalid directory input: {base_directory}")
            print(f"'{base_directory}' is not a valid directory. Please try again.")


def identify_directory_type(base_directory: Path) -> Optional[str]:
    if "instagram" in base_directory.name.lower().strip():
        if (base_directory / "index.html").exists():
            return "Instagram HTML"
        else:
            return "Instagram JSON"
    elif any(
            file.suffix == ".xz" and len(file.suffixes) > 1 and file.suffixes[-2] == ".json"
            for file in base_directory.glob("*.*")
    ):
        return "Compressed JSON"
    return None


def execute_script(script_path: Path, base_directory: Path):
    try:
        logging.info(f"Executing {script_path}...")
        result = subprocess.run(
            ["python", str(script_path), str(base_directory)],
            capture_output=True,
            text=True,
            check=True,
        )
        logging.info(f"Script output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred while executing {script_path}:\n{e.stderr}")


def csv_folder_exists():
    csv_folder = Path(__file__).parent / "csv"
    if not csv_folder.exists():
        csv_folder.mkdir()
        logging.info(f"'csv' folder created at: {csv_folder}")
    else:
        logging.info(f"'csv' folder already exists at: {csv_folder}")


# def main():
#     setup_logging()
#     csv_folder_exists()
#     base_directory = get_valid_base_directory()
#     logging.info(f"Using base directory: {base_directory}")
#     directory_type = identify_directory_type(base_directory)
#     if not directory_type:
#         logging.error("Unable to identify the directory type.")
#         return
#     logging.info(f"Detected directory type: {directory_type}")
#     if directory_type == "Instagram JSON":
#         confirm = input("Is this an Instagram JSON directory? (Y/N): ").strip().lower()
#         if confirm == "y":
#             logging.info("Confirmed directory type: Instagram JSON")
#             content_script_path = Path(__file__).parent / "instagram_json_content.py"
#             inbox_script_path = Path(__file__).parent / "instagram_json_inbox.py"
#             execute_script(content_script_path, base_directory)
#             execute_script(inbox_script_path, base_directory)
#         else:
#             logging.warning("Directory type confirmation declined.")
#     else:
#         logging.warning(f"No script configured for directory type: {directory_type}")
def main():
    while True:
        setup_logging()
        csv_folder_exists()
        base_directory = get_valid_base_directory()
        logging.info(f"Using base directory: {base_directory}")
        directory_type = identify_directory_type(base_directory)
        if not directory_type:
            logging.error("Unable to identify the directory type.")
            return
        logging.info(f"Detected directory type: {directory_type}")
        if directory_type == "Instagram JSON":
            confirm = input(
                "Is this an Instagram JSON directory?\n"
                "Press 'enter' or type 'y' then press enter to confirm yes.\n"
                "If it isn't, type 'n' to continue to select directory type manually.\n"
                "Or type 'r' to re-enter the base directory: "
            ).strip().lower()
            if confirm == "y" or confirm == "":
                logging.info("Confirmed directory type: Instagram JSON")
                content_script_path = Path(__file__).parent / "instagram_json_content.py"
                inbox_script_path = Path(__file__).parent / "instagram_json_inbox.py"
                repair_script_path = Path(__file__).parent / "file_repair.py"
                apply_script_path = Path(__file__).parent / "apply.py"

                input(
                    f"\nPress 'enter' to run the appropriate scripts for the directory type: {directory_type}.\n"
                    "Scripts that will be run:\n"
                    "1. instagram_json_content.py\n"
                    "2. instagram_json_inbox.py\n"
                )

                execute_script(content_script_path, base_directory)
                logging.info("Finished running instagram_json_content.py")

                execute_script(inbox_script_path, base_directory)
                logging.info("Finished running instagram_json_inbox.py")

                input(
                    "\nThe initial scripts have completed successfully.\n"
                    "Press 'enter' to proceed with running file_repair.py."
                )

                execute_script(repair_script_path, base_directory)
                logging.info("Finished running file_repair.py.")

                input(
                    "\nThe file repair script has completed successfully.\n"
                    "Press 'enter' to proceed with running apply.py."
                )

                execute_script(apply_script_path, base_directory)
                logging.info("Finished running apply.py. The process is complete.")
                break
            elif confirm == "r":
                logging.info("User chose to re-enter the base directory.")
                continue
            else:
                logging.warning("Directory type confirmation declined.")
        else:
            logging.warning(f"No script configured for directory type: {directory_type}")
        break

if __name__ == "__main__":
    main()
