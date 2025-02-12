import os

options = {
    "1": "Procedural Programming",
    "2": "Object-Oriented Programming",
    "3": "Functional Programming",
    "4": "Imperative Programming",
    "5": "Reflective Programming",
    "6": "Scripting Language Paradigm",
    "7": "Modular Programming"
}

structures = {
    "1": ["main.py", "utilities.py", "README.md"],
    "2": ["models/user.py", "models/product.py", "main.py", "README.md"],
    "3": ["main.py", "data_transforms.py", "utils.py", "README.md"],
    "4": ["main.py", "tasks.py", "README.md"],
    "5": ["core/base_model.py", "core/field.py", "models/user.py", "models/product.py", "main.py", "README.md"],
    "6": ["script1.py", "script2.py", "shared.py", "README.md"],
    "7": ["module1/main.py", "module1/utils.py", "module2/main.py", "module2/utils.py", "main.py", "README.md"]
}


def create_structure(base_path, structure):
    for path in structure:
        full_path = os.path.join(base_path, path)
        directory = os.path.dirname(full_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(full_path):
            with open(full_path, 'w') as file:
                pass  # creates an empty file


def main():
    while True:
        print("Please choose an option:")
        for option, name in options.items():
            print(f"    {option}: {name}")

        choice = input("Your choice: ")

        if choice not in options:
            print("    Invalid choice, please try again.")
            continue

        print(f"You selected: {options[choice]}")
        print("Folder structure:")
        for path in structures[choice]:
            print(f"    - {path}")

        create = input("Do you want to create this folder structure? (yes/no): ")
        if create.lower() == "yes":
            base_path = input("Where do you want to create it? (default: ~/python_tutorial/init/workspace/temporary): ")
            if base_path == "":
                base_path = "~/python_tutorial/init/workspace/temporary"

            base_path = os.path.expanduser(base_path)  # expands ~ to the user's home directory
            create_structure(base_path, structures[choice])

        again = input("Do you want to start over? (yes/no): ")
        if again.lower() != "yes":
            break


if __name__ == "__main__":
    main()