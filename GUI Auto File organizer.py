import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Define the file extensions and their corresponding folders
extension_lists = {
    "Documents": [".doc", ".docx", ".pdf", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv"],
    "Music": [".mp3", ".wav", ".flac", ".ogg"],
    "Other": []
}

other_folder = os.path.join(os.environ["USERPROFILE"], "Other")

def organize_files():
    """
    Organizes files in the selected directory based on their file extensions.
    """
    selected_dir = filedialog.askdirectory(title="Select Directory")
    if selected_dir:
        for filename in os.listdir(selected_dir):
            filepath = os.path.join(selected_dir, filename)
            move_file(filepath, extension_lists)
        print("File organization complete!")

def move_file(filepath, extension_lists):
    """
    Checks the file extension and moves the file to the appropriate folder.

    Args:
        filepath (str): The full path of the file to be moved.
        extension_lists (dict): A dictionary of file extensions and their corresponding folders.
    """
    filename = os.path.basename(filepath)
    script_path = os.path.abspath(__file__)
    extension = os.path.splitext(filename)[1].lower()

    if filepath != script_path:  # Check if it's not the script itself
        for folder_name, extensions in extension_lists.items():
            if extension in extensions:
                folder_path = os.path.join(os.environ["USERPROFILE"], folder_name)
                # Create folder if it doesn't exist
                os.makedirs(folder_path, exist_ok=True)
                destination = os.path.join(folder_path, filename)
                try:
                    shutil.move(filepath, destination)
                    print(f"Successfully moved {filename} to {folder_name}")
                except OSError:
                    # If the source and destination are on different disk drives, copy and then delete
                    shutil.copy2(filepath, destination)
                    os.remove(filepath)
                    print(f"Successfully copied {filename} to {folder_name}")
                return

        # Move to 'Other' folder if extension not found
        destination = os.path.join(other_folder, filename)
        try:
            shutil.move(filepath, destination)
            print(f"File type not recognized. Moved {filename} to Other")
        except OSError:
            shutil.copy2(filepath, destination)
            os.remove(filepath)
            print(f"File type not recognized. Copied {filename} to Other")
    else:
        print(f"Skipping {filename} (script itself)")

def main():
    root = tk.Tk()
    root.title("GUI Auto File Organizer")

    organize_button = ttk.Button(root, text="Organize Files", command=organize_files)
    organize_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
