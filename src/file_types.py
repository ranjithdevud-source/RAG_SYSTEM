import os
from collections import defaultdict
from google.cloud import storage

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

    def categorize_file(self,bucket_name):
        """
        Categorize file based on extension
        """
        # _, ext = os.path.splitext(file_path)
        # ext = ext.lower()

        # for category, extensions in self.FILE_CATEGORIES.items():
        #     if ext in extensions:
        #         self.categorized_files[category].append(file_path)
        #         return

        # self.categorized_files["Others"].append(file_path)

        client = storage.Client()
        blobs = client.bucket(bucket_name).list_blobs()
        for blob in blobs:
            _, ext = os.path.splitext(blob.name)
            ext = ext.lower()
            blob_name = blob.name
            for category, extension in self.FILE_CATEGORIES.items():
                if ext in extension:
                    self.categorized_file[category].append(blob_name)
            else:
                self.categorized_file["Others"].append(blob_name)
# Manual download from GCP & parse
    # def read_blob(self,blob_name: str):
        
    #     return self._bucket.blob(blob_name).download_as_bytes()
    
#     def scan_folder(self, folder_path, level=0):
#         """
#         Recursively scan folders and files
#         """
#         client = storage.Client()
#         blobs = client.bucket(folder_path).list_blobs()
#         for blob in blobs:
#             _, ext = os.path.splitext(blob.name)
#             ext = ext.lower()
#             blob_name = blob.name
#             for category, extension in self.FILE_CATEGORIES.items():
#                 if ext in extension:
#                     self.categorize_file[category].append(blob_name)
#                 else:
#                     self.categorize_file["Others"].append(blob_name)
# '''
#         try:
         
'''
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
    #             print(file) '''