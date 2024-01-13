# util_api.py

import dotenv
import os
import pathlib


def get_api_key() -> str:
    dotenv.load_dotenv()
    api_key = os.getenv("API_KEY")

    if not api_key:  # Check for None and empty string
        return (
            "API_KEY not found or is empty in the .env file. Please ensure you have a .env file in your "
            "project directory with the content 'API_KEY=your_api_key_here'."
        )
    else:
        gitignore_message = (
            "Good job! Your .env file is listed in your .gitignore."
            if is_env_in_gitignore()
            else (
                "IMPORTANT: Add your .env file to your .gitignore to keep your API key secure."
            )
        )
        print(gitignore_message)
        return api_key


def get_ignore_file() -> str:
    """
    Return the path to the .gitignore file in my parent directory.
    """
    return pathlib.Path.cwd().parent.joinpath(".gitignore")


def is_env_in_gitignore() -> bool:
    """
    Check if '.env' is listed in the '.gitignore' file.
    """
    try:
        with open(get_ignore_file(), "r") as file:
            for line in file:
                if ".env" in line:
                    return True
    except FileNotFoundError:
        pass  # .gitignore not found

    return False


def main() -> None:
    api_key: str = get_api_key()
    print(api_key)


if __name__ == "__main__":
    main()
