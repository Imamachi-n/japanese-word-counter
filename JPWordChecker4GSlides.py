# coding: utf-8
#! env/bin/python3

from __future__ import print_function
import unicodedata
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

# FIXME: ここを適宜修正！
# ["Google Slides の ID", "タイトル（任意の値でOKです）"]
PRESENTATION_ID_LIST = [
    ['XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'React JP'],
    ['YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY', 'Vue JP'],
    ['ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', 'XXX JP']
]


def is_japanese(char):
    try:
        name = unicodedata.name(char)
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    except:
        # 絵文字などでエラーになるケースがある（ごくまれ）
        # print(char)
        pass
    return False


def getSlideInfo(service, id):
    # Call the Slides API
    presentation = service.presentations().get(
        presentationId=id[0]).execute()
    slides = presentation.get('slides')

    counter = 0
    jp_chars = ""
    for char in str(slides):
        if is_japanese(char):
            counter += 1
            jp_chars += char

    url = "https://docs.google.com/presentation/d/" + id[0]
    print(id[1], counter, jp_chars, url, sep="\t")


def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elments in a sample presentation.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokenSlides.pickle'):
        with open('tokenSlides.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_slides.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('tokenSlides.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('slides', 'v1', credentials=creds)
    for id in PRESENTATION_ID_LIST:
        getSlideInfo(service, id)


if __name__ == '__main__':
    main()
