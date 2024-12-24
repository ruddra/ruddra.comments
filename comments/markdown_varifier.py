import os
import yaml
import mistune

def read_yml_files(root_dirs):
    """Read all .yml files from specified directories."""
    yml_data = []
    for root_dir in root_dirs:
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.yml'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            yml_data.append((file_path, data))
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
    return yml_data

def is_valid_markdown(comment):
    """Check if the given comment is valid Markdown."""
    try:
        # Use mistune to parse the Markdown
        mistune.create_markdown()(comment)
        return True
    except Exception as e:
        print(f"Invalid Markdown: {e}")
        return False

def process_yml_files(root_dirs):
    """Process YML files and verify the structure."""
    yml_files = zip(root_dirs, read_yml_files(root_dirs))
    for root_dir, (file_path, data) in yml_files:

                if all(key in data.keys() for key in ["_id", "_parent", "reply_to", "comment", "name", "email", "avatar", "date"]):
                    comment = data.get("comment", "")
                    if isinstance(comment, str):
                        if is_valid_markdown(comment):
                            if comment.count('"') % 2 != 0:
                                raise Exception(f"Unbalanced single quotes in file data/comments/comments/{file_path}")
                            
                        else:
                            raise Exception(f"Invalid Markdown in file data/comments/comments/{file_path}: {comment}")
                    else:
                        raise Exception(f"Comment is not a string in file data/comments/comments/{file_path}")
                else:
                    raise Exception(f"Missing keys in file data/comments/comments/{file_path}: {data.keys()}")

if __name__ == "__main__":
    # Specify the directories containing the YML files
    current_path = os.getcwd()  # Get the current working directory
    folders = [f for f in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, f))]
    process_yml_files(folders)