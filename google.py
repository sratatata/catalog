
from __future__ import print_function
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class GoogleSpreadsheetHelper(object):
    """Helper used to create and modify google spreadsheet"""

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    SCOPES += ' https://www.googleapis.com/auth/drive.metadata'
    SCOPES += ' https://www.googleapis.com/auth/drive'
    SCOPES += ' https://www.googleapis.com/auth/drive.file'
    SCOPES += ' https://www.googleapis.com/auth/drive.appdata'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    def __init__(self, store_file_name):
        self.__flags = tools.argparser.parse_args(args=[])
        self.credentials = self.__get_credentials(store_file_name)
        self.http = self.credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v2', http=self.http)
        discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                         'version=v4')
        self.spreadsheet_service = discovery.build('sheets', 'v4', http=self.http,
                                  discoveryServiceUrl=discovery_url)

    def __get_credentials(self, store_file_name):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, store_file_name)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(GoogleSpreadsheetHelper.CLIENT_SECRET_FILE,
                                                  GoogleSpreadsheetHelper.SCOPES)
            flow.user_agent = GoogleSpreadsheetHelper.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags=self.__flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    def create_new(self, name, sheets):
        """Creates new spreadsheet file"""
        props = []
        for sh in sheets:
            props.append({
                'properties' : {
                    'title' : sh
                }
            })
        body = {
            'properties': {
                'title' : name
            },
            'sheets': props,
        }
        
        spreadsheet_file = self.spreadsheet_service.spreadsheets().create(body=body).execute(http=self.http)
        return spreadsheet_file['spreadsheetId']

    def append_row(self, spreadsheet_id, range_name, cells):
        """Appends new row to document"""
        values = [cells]
        body = {
            'values': values
        }
        value_input_option = "RAW"
        result = self.spreadsheet_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        return result['updates']['updatedRows']

    def get_headers(self, spreadsheet_id, range_name):
        """Returns header cells"""
        result = self.spreadsheet_service.spreadsheets().values().get(
            spreadsheetId = spreadsheet_id, range=range_name).execute()
        return result.get('values', [])[0]
    
    def get_last_index(self, spreadsheet_id, range_name):
        """Returns last row #index value"""
        result = self.spreadsheet_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        v = values[len(values)-1][0]
        return v