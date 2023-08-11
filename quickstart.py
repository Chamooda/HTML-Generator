from __future__ import print_function

import os.path
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '' #In the URL of the spreadsheet copy the part after /d/ and before /edit
SAMPLE_RANGE_NAME = 'Class Data!'


def Update_Sequence():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,    
        range='Sheet1').execute()   #Sample Spreadsheet has been defined few lines prior
        #Range here is the sheet name like the differnt sheets in one file you can switch between from the bottom of the page
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return
        

        from bs4 import BeautifulSoup

        path = "D:/dynamic_webpage/templates/dynamicindex.html"
        
        with open(path, 'r') as f:
            html = f.read()

        pattern = "<!-- Addons insertion -->"
        match = re.search(pattern, html)
        start = (match.end() + 1)


        html = html[:start]

        end_String = "</swiper-container><script src=\"https://cdn.jsdelivr.net/npm/swiper@10/swiper-element-bundle.min.js\"></script><!-- THis is form where the rest of the program begins --><script src=\"https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js\"></script><script src=\"dynamic.js\"></script>"
        
        
        for row in values:
            name = row[0]
            desc = row[1]
            img_url = row[2]


            Update = f"<swiper-slide><div class=\"container\"><div class=\"polaroid\"><a href=\"#\" title=\"{name}\"><img alt=\"Santorini\" height=\"250\" src=\"{img_url}\" title=\"{name}\"/></a><p style=\"color: aliceblue;\"> {desc}</p></div></div></swiper-slide>"

            html = html + Update
            #loop ends here

        html = html + end_String + "</body></html>"

        soup = BeautifulSoup(html, 'html.parser')

        """Methods appending to the body of the html file will not work
        as body will be a class tag element and not a string
        Appending will result in unusual formatting to be applied to the html file"""
        #body = soup.find('body')
        #body.append(Update)

        with open(path,'w') as f:
            f.write(str(soup))
        print('Updated')

        
        
    except HttpError as err:
        print(err)

    

#__Main__
Update_Sequence()
