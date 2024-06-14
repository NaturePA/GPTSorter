import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import os
from file_categorizer import FileCategorizer
from file_mover import FileMover
from config import DEFAULT_DIRECTORY

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        root.title("File Sorter")

        self.selected_directory = DEFAULT_DIRECTORY
        self.files = []
        self.file_folder_mapping = {}

        # Frame for Directory Selection
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        # Directory Selection Button
        self.btn_select_dir = tk.Button(self.frame, text="Select Directory", command=self.select_directory)
        self.btn_select_dir.pack(side=tk.LEFT)

        # Button for Categorizing Files
        self.btn_categorize = tk.Button(self.frame, text="Categorize Files", command=self.categorize_files)
        self.btn_categorize.pack(side=tk.LEFT)

        # Button for Organizing Files
        self.btn_organize = tk.Button(self.frame, text="Organize Files", command=self.organize_files)
        self.btn_organize.pack(side=tk.LEFT)

        # Listbox to display files
        self.lst_files = Listbox(root, width=60, height=15)
        self.lst_files.pack(padx=10, pady=10)

        # Text widget to display and edit folder suggestions
        self.txt_folder_suggestions = tk.Text(root, height=15, width=60)
        self.txt_folder_suggestions.pack(padx=10, pady=10)

    def select_directory(self):
        # Open file dialog to select directory
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.list_files_in_directory(directory)

    def list_files_in_directory(self, directory):
        # Clear the listbox
        self.lst_files.delete(0, tk.END)
        self.files = []

        # List files in the directory and add to the listbox
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)):
                self.files.append(file)
                self.lst_files.insert(tk.END, file)

    def categorize_files(self):
        if not self.files:
            messagebox.showinfo("No Files", "No files to categorize. Please select a directory first.")
            return

        categorizer = FileCategorizer()
        folder_suggestions = categorizer.get_folder_suggestions(self.files)

        # Display folder suggestions in the Text widget
        self.txt_folder_suggestions.delete("1.0", tk.END)
        self.txt_folder_suggestions.insert("1.0", folder_suggestions)

        messagebox.showinfo("Categorization Complete", "Files have been categorized.")

    def organize_files(self):
        edited_folder_suggestions = self.txt_folder_suggestions.get("1.0", tk.END)
        self.file_folder_mapping = self.parse_folder_suggestions(edited_folder_suggestions)

        if not self.file_folder_mapping:
            messagebox.showinfo("No File Organization", "No file organization to perform.")
            return

        mover = FileMover(self.selected_directory)
        mover.move_files(self.file_folder_mapping)
        messagebox.showinfo("Organization Complete", "Files have been organized.")

        self.list_files_in_directory(self.selected_directory)

    def parse_folder_suggestions(self, suggestions_text):
        file_folder_mapping = {}
        lines = suggestions_text.strip().split("\n")
        current_folder = None

        for line in lines:
            if line.startswith("Folder:"):
                current_folder = line.replace("Folder:", "").strip()
            elif line.startswith("Files:") and current_folder:
                files = line.replace("Files:", "").split(",")
                files = [file.strip() for file in files if file.strip()]
                file_folder_mapping[current_folder] = files
                current_folder = None

        return file_folder_mapping

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()