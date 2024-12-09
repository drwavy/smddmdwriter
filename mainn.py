# new main, in dev
from pathlib import Path

def get_valid_base_dir():
    while True:
        base_dir = input("Enter the base directory: ").strip()
        base_path = Path(base_dir)
        if base_path.is_dir():
            with open("base_dir.txt", "w") as file:
                file.write(str(base_path))
                file.flush()
            print(f"Base directory saved to base_dir.txt: {base_path}")
            return base_path
        else:
            print(f"'{base_dir}' is not a valid directory. Please try again.")

def display_menu():
    while True:
        print("\n=== Social Media Data Download Type ===")
        print("Option 1: Instagram  HTML")
        print("Option 2: Instagram  JSON")
        print("Option 3: Another option")
        print("4. Exit")
        choice = input("Enter Social Media Data Download Type Option Choice Number: ").strip()
        if choice == "1":
            print("You chose Option 1: Performing action...")
        elif choice == "2":
            print("You chose Option 2: Performing another action...")
        elif choice == "3":
            print("You chose Option 3: Performing yet another action...")
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    base_dir = get_valid_base_dir()
    print(f"Using base directory: {base_dir}")
    display_menu()

if __name__ == "__main__":
    main()
