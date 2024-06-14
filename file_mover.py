import os
import shutil

class FileMover:
    def __init__(self, base_directory):
        self.base_directory = base_directory

    def interpret_folder_suggestions(self, suggestion_text):
        file_folder_mapping = {}
        current_folder = None
        for line in suggestion_text.split('\n'):
            if line.startswith('Folder:'):
                current_folder = line.replace('Folder:', '').strip()
            elif line.startswith('Files:') and current_folder:
                files = line.replace('Files:', '').split(',')
                files = [f.strip() for f in files]
                file_folder_mapping[current_folder] = files
                current_folder = None
        return file_folder_mapping

    def move_files(self, file_folder_mapping):
        for folder, files in file_folder_mapping.items():
            folder_path = os.path.join(self.base_directory, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for file in files:
                source_path = os.path.join(self.base_directory, file)
                destination_path = os.path.join(folder_path, file)

                # Check if the file exists to avoid errors
                if os.path.exists(source_path):
                    shutil.move(source_path, destination_path)
                    print(f"Moved {file} to {folder}")
                else:
                    print(f"File not found: {source_path}")

# Example usage
if __name__ == "__main__":
    mover = FileMover('/path/to/your/desktop')  # Replace with the actual path
    suggestion_text = "..."  # Replace with the folder suggestion text from GPT
    file_folder_mapping = mover.interpret_folder_suggestions(suggestion_text)
    mover.move_files(file_folder_mapping)
