import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from GetStats import getOpponent



class Sheet:
    VAR_COUNT = 1
    # I didnt write any of this code so i cant comment it, refreshes api access somehow?
    @staticmethod
    def gsheetApiCheck(SCOPES):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    

    @staticmethod
    def pushSheetData(zone, data):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SPREADSHEET_ID = '1PhKd7v2ydqVTw3osRN7G9Vtd264ENbLSJ1-46L7yUPA'
        creds = Sheet.gsheetApiCheck(SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=zone, valueInputOption='USER_ENTERED', body=data).execute()


    @staticmethod
    def pullSheetData(DATA_TO_PULL):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SPREADSHEET_ID = '1PhKd7v2ydqVTw3osRN7G9Vtd264ENbLSJ1-46L7yUPA'
        creds = Sheet.gsheetApiCheck(SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()


        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=DATA_TO_PULL).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
        else:
            rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=DATA_TO_PULL).execute()
            data = rows.get('values')
            return data
    
    @staticmethod
    def pullVars():
        vars = {}
        data = Sheet.pullSheetData(f"BotVars!A1:B{Sheet.VAR_COUNT}")
        for i in data:
            vars[i[0]] = i[1]

        return vars

    @staticmethod
    def pushVars(vars):
        newVars = []
        for i, j in vars.items():
            # newVars.append([i, j])
            newVars.append(i)
            newVars.append(j)
        print(newVars)
        body = {'values':vars}
        Sheet.pushSheetData(f"BotVars!A1:C{Sheet.VAR_COUNT + 1}", body)
        


    @staticmethod
    def setupGame(date):
        startCell = None

if __name__ == "__main__":
    
    v = Sheet.pullVars()
    v["GamesPlayed"] = 1
    Sheet.pushVars(v)