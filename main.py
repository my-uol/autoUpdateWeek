from dotenv import load_dotenv
from github import Auth
from github import Github
import os
import re

load_dotenv()

GIT_TOKEN = os.getenv("GIT_TOKEN")

auth = Auth.Token(GIT_TOKEN)

g = Github(auth=auth)

def open_file(old_edit, new_edit):
    try:
        with open("toEdit.md", "r") as f:
            content = f.read()

        updated_content = content.replace(old_edit, new_edit)
        
        with open("toEdit.md", "w") as f:
            f.write(updated_content)
    except Exception as e:
        print(f"Error updating file: {e}")

def get_current_week_from_file():
    try:
        with open("toEdit.md", "r") as f:
            content = f.read()

        match = re.search(r'current_week-(\d+)', content)
        if match:
            return match.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_file():
    desired_week = input("What week is it? ")
    old_week_str = "current_week-"
    current_week = get_current_week_from_file()
    if current_week is not None:
        old_week_full_str = f"{old_week_str}{current_week}"
        new_week_full_str = f"{old_week_str}{desired_week}"
        open_file(old_week_full_str, new_week_full_str)


def commit_file():
    try:
        repo = g.get_repo("my-uol/.github")
        contents = repo.get_contents("profile/README.md", ref="main")
        with open("toEdit.md", "r") as f:
            new_content = f.read()
        commit_message = "Update Week"
        repo.update_file(contents.path, commit_message, new_content, contents.sha, branch="main")
    except Exception as e:
        print(f"Error committing file: {e}")

def main():
    write_file()
    commit_file()

if __name__ == "__main__":
    main()
    print("Done!")
    g.close()



