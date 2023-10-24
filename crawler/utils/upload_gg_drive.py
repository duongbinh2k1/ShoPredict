from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from io import StringIO


class GGDrive:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GGDrive, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.gauth = GoogleAuth()
        self.credentials_file = 'client_secrets.json'
        self.drive = None

    def authenticate(self):
        try:
            self.gauth.LoadCredentialsFile(self.credentials_file)

            if self.gauth.credentials is None or self.gauth.access_token_expired:
                self.gauth.LocalWebserverAuth()
                self.gauth.Authorize()
                self.gauth.SaveCredentialsFile(self.credentials_file)

            self.drive = GoogleDrive(self.gauth)
            print("Authenticate gg drive success !!!")
        except Exception as e:
            print(f"Error authenticate gg drive: {str(e)}")

    def upload_csv(self, csv_data, title, folder_name="shopredict"):
        if not self.drive:
            print("Error")
            return

        try:
            csv_content = StringIO()
            csv_data.to_csv(csv_content, index=False)
            csv_file = self.drive.CreateFile({'title': title})
            csv_file.Upload()
            print(f"Uploaded '{title}' successfully.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def read_csv(self, title):
        if not self.drive:
            print("Error")
            return None

        try:
            file_list = self.drive.ListFile({'q': f"title = '{title}' and trashed=false"}).GetList()
            if file_list:
                file = file_list[0]
                content = file.GetContentString()
                df = pd.read_csv(StringIO(content))
                return df
            else:
                print(f"Cannot find file'{title}' in storage")
        except Exception as e:
            print(f"Error: {str(e)}")

    # def list_files_in_folder(self, folder_name="shopredict"):
    #     if not self.drive:
    #         print("Error")
    #         return []

    #     try:
    #         folder_id = None
    #         file_list = self.drive.ListFile({'q': f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"}).GetList()
    #         if file_list:
    #             folder_id = file_list[0]['id']
    #             files = self.drive.ListFile({'q': f"'{folder_id}' in parents and trashed = false"}).GetList()
    #             return files
    #         else:
    #             print(f"Folder '{folder_name}' not found.")
    #             return []
    #     except Exception as e:
    #         print(f"Error: {str(e)}")
    #         return []
