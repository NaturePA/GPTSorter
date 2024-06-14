from config import client, DEFAULT_DIRECTORY  # Import the instantiated client from the config
import os  # Ensuring it's here if needed for file system operations

class FileCategorizer:
    def __init__(self):
        # The API key is now managed directly within the client instance from config.py
        self.client = client

    def list_files_in_directory(self, directory):
        # List files in the given directory
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    def get_folder_suggestions(self, files):
        prompt = (f"I have a list of files: {', '.join(files)}. Please suggest a way to organize "
                "these files into folders in the following format: \n"
                "Folder: [Folder Name]\nFiles: [file1, file2, file3]\n\n"
                "For example, if you think 'file1.jpg' and 'file2.png' should go into a folder named 'Images', "
                "the response should be:\nFolder: Images\nFiles: file1.jpg, file2.png")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            # Check if the response has a 'choices' attribute and it is not empty
            if hasattr(response, 'choices') and response.choices:
                # Assuming the choices are available in a list-like object with an attribute access
                # Each choice should be a ChatCompletionMessage object
                first_choice = response.choices[0]  # Get the first choice
                if hasattr(first_choice, 'message') and hasattr(first_choice.message, 'content'):
                    return first_choice.message.content.strip()
                else:
                    print("Message content is not available in the expected format.")
                    return "Unexpected message content format"
            else:
                print("No choices available in the response.")
                return "No choices in response"
        except Exception as e:
            print(f"Error in getting folder suggestions: {e}")
            return "Error in folder suggestion"

# Example usage
if __name__ == "__main__":
    categorizer = FileCategorizer()  # No need to pass API key; it's managed in the client instance
    files = categorizer.list_files_in_directory(DEFAULT_DIRECTORY)
    folder_suggestions = categorizer.get_folder_suggestions(files)
    print(folder_suggestions)