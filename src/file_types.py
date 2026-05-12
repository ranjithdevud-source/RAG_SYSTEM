import os
from collections import defaultdict

class DataSource():
    def __init__(self):
    
    # Root folder path
        self.ROOT_FOLDER = r"C:\Users\RanjithBalasubramani\OneDrive - IBM\Desktop\AI\Mistral AI\RAG\KT document"

    # File type categories
        self.FILE_CATEGORIES = {
        "PDF": [".pdf"],
        "Excel": [".xls", ".xlsx"],
        "CSV": [".csv"],
        "Word": [".doc", ".docx"],
        "Text": [".txt"],
        "PowerPoint": [".ppt", ".pptx"],
        "Images": [".png", ".jpg", ".jpeg", ".gif"],
        "JSON": [".json"],
        "XML": [".xml"],
        "Code": [".py", ".java", ".js", ".cpp", ".c", ".cs"],
    }

    # Store categorized files
        self.categorized_files = defaultdict(list)

    # Store folder structure
        self.folder_structure = []

    def categorize_file(self,file_path):
        """
        Categorize file based on extension
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        for category, extensions in self.FILE_CATEGORIES.items():
            if ext in extensions:
                self.categorized_files[category].append(file_path)
                return

        self.categorized_files["Others"].append(file_path)

    def scan_folder(self, folder_path, level=0):
        """
        Recursively scan folders and files
        """

        try:
            items = os.listdir(folder_path)

            for item in items:
                item_path = os.path.join(folder_path, item)

                # Handle subfolders
                if os.path.isdir(item_path):
                    self.folder_structure.append(
                        f'{"    " * level}[Folder] {item}'
                    )

                    # Recursive call
                    self.scan_folder(item_path, level + 1)

                # Handle files
                elif os.path.isfile(item_path):
                    self.folder_structure.append(
                        f'{"    " * level}[File] {item}'
                    )

                    self.categorize_file(item_path)

        except Exception as e:
            print(f"Error scanning {folder_path}: {e}")

    # Start scanning (below codes are mofed to the indexing.py)
    # scan_folder(self.ROOT_FOLDER)

    # Print folder structure
    # print("\n===== FOLDER STRUCTURE =====")

    # for line in self.folder_structure:
    #     print(line)

    # Print categorized files
    # print("\n===== CATEGORIZED FILES =====")

    # for category, files in categorized_files.items():
    #     print(f"\n--- {category} ---")
    #     if category == 'PDF':
    #         for file in files:
    #             print(file)