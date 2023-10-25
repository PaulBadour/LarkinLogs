from GetStats import getOpponent
import gspread
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Sheet:
    GAME_PLAYED_SPOT = 'B1'
    def __init__(self):
        cred = gspread.service_account("cred.json")
        self.sheet = cred.open_by_key('1PhKd7v2ydqVTw3osRN7G9Vtd264ENbLSJ1-46L7yUPA')
        

    def setupGame(self, date):
        gp = int(self.sheet.get_worksheet(2).acell(Sheet.GAME_PLAYED_SPOT).value)
        startCell = (6 * gp) + 4
        
        

        data = [
            [f"{date} (v. {getOpponent(date)})", '', '','','','',''],

        ]    

        self.sheet.get_worksheet(0).update(f'A{startCell}:G{startCell + 4}')

if __name__ == '__main__':
    s = Sheet()
    