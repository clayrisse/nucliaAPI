import os
import requests
import sys
import mimetypes
import urllib3
from dotenv import load_dotenv
print("...............Wellcome to Claudia's Test ;)...............")

urllib3.disable_warnings()

IGNORE = [
    ".DS_Store",
    "Thumbs.db",
]

# BACKEND = "https://europe-1.nuclia.cloud/api/v1"
# KNOWLEDGE_BOX = "/kb/fae260b8-b03d-4708-9ca5-74f4159872a7"
# API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InNhIn0.eyJpc3MiOiJodHRwczovL251Y2xpYS5jbG91ZC8iLCJleHAiOjE3MTI5Mjk5OTAsImlhdCI6MTY4MTMwNzU5MCwic3ViIjoiYzRjMzc3MmUtNDdlMC00ZWYyLWI1ZjktMzY0NDY4ZjY3OWI4IiwianRpIjoiNWY4YTUyOTQtNzdiZi00ZDBiLTgyMGQtZWUwNGU4ZTA5MTRiIiwia2V5IjoiMTYzODQxYWUtNWFmMi00MmY0LWFkMjEtMzYwNDI2MWYzNjI1Iiwia2lkIjoiY2Y2N2EzMTgtNTg4MS00MDc2LWJhOGUtZWQ2YTVmZmJhNjczIn0.QlJUK8UKVTa1d80eZOsfj8yOin6l7Ee6ITgQzbVsi3Sz12-8zXdljbyQo9fqWLu3eEhzsAlZTDGKdiJbsDUsiXBfdGFX56e7dYni4TxGcoxHfbPJzqG7QhmcikW3cQt10h6zT4xmpZ3oYTkmEmaSSO98neCf93FIausVoOKLfKFsD981GfTTC6XfmlIcZo9FOtFocXupqYYj_hD9a3RSKUHf9053_Ou0MAhfFsu85KEjs2-LjGI4tZVA-4N8RP0TH26q3oXROId4mPsKbsO-Ty-wY6YB5x5BJHU64-MW-X_Si66JglKURr4yKjWDSky-yag71nPn0Y_X8h-MeP4--Tl-tMYo2IbSvakJwI9UyvELMo7rzbTsoKpjJQjv_YP3XA10thIZCPg5dkSAf2ITcnooV3FruTVf4OyZ5hrHpzIvSQ8DfJ19ALfdNUYh9VGgOVtSFTtzctiZuhBFqbDFkKwcXQgmQSd4AKYUcLpH8zguYEusUxC_v74MPP03IBvSyU1QFVhIPEiZPXoBaCXfh2IJGip0juN82LhPSyOsnqjXP4FtmuKKoTzQq23z1nHbPkG9IcErjARM1sfIKpfaA3egnx42snR2MCKosUyLQ6YQ6UobYgw0LDvWjkDyba9gY5sAZnggVVWH-lSk3UHH6_pf81obO2Lw1UaA-6a1ftQ"


def load_api_key_and_box():
    print("loading enviorment keys...")
    load_dotenv()


def upload_file(content_path):
    file_name = os.path.basename(content_path).encode('ascii')
    file_upload_path = f'{os.getenv("BACKEND")}{os.getenv("KNOWLEDGE_BOX")}/upload'
    print(f'Importing {content_path} at {file_upload_path}')

    with open(content_path, "rb") as source_file:
        response = requests.post(
            file_upload_path,
            headers={
                "content-type": mimetypes.guess_type(content_path)[0] or "application/octet-stream",
                "x-filename": file_name,
                "X-STF-Serviceaccount": "Bearer " + os.getenv("API_KEY"),
                "x-synchronous": "true",
            },
            data=source_file.read(),
            verify=False,
        )
        if response.status_code != 201:
            print(f'Error {response.status_code} importing {file_name}')


def upload_folder(path, processed_labels=[]):
    all_files = os.listdir(path)
    for content in all_files:
        if content in IGNORE or content.startswith("."):
            continue
        content_path = os.path.join(path, content)
        if os.path.isdir(content_path):
            processed_labels.extend(upload_folder(
                content_path, processed_labels))
        else:
            if str(os.path.basename(content_path).encode('ascii')) in processed_labels:
                print("\n---The file: ", os.path.basename(content_path).encode('ascii'),
                      " is already processing. It might be duplicated and won't be uploaded. \n---Check you dont have a copy in another folder or change the name in one of the files.\n")
            else:
                # this "processed labels" keeps track of all the file names uploaded and prevents duplicates when asked
                # it needs to be passed out so that can keep track in the recursion function
                processed_labels.append(str(os.path.basename(
                    content_path).encode('ascii')))
                upload_file(content_path)

    return processed_labels


if __name__ == "__main__":
    root = sys.argv[1]
    load_api_key_and_box()
    upload_folder(root)
    print("\n---------- All files and folders found have been uploaded :) ----------")
#
