from GetStats import getOpponent, getPlayerPoints
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
        self.sheet.get_worksheet(2).update('B1', gp + 1)
        

        data = [
            [f"{date} (v. {getOpponent(date)})", '', '','','','',''],

        ]    

        self.sheet.get_worksheet(0).update(f'A{startCell}:G{startCell + 4}')

    def addPointStats(self, date):
        gp = int(self.sheet.get_worksheet(2).acell(Sheet.GAME_PLAYED_SPOT).value)
        #pa = int(self.sheet.get_worksheet(2).acell('B7').value)
        stats = getPlayerPoints(date)
        data = [date]

        # pointedPlayers = [i for i in stats.keys() if stats[i] > 0][1:]
        listedPlayers = self.sheet.get_worksheet(1).row_values(1)[1:]
        #input(listedPlayers)
        for i in range(len(listedPlayers)):
            name = listedPlayers[i]
            try:
                p = stats[name.lower()]
                del stats[name.lower()]
            except KeyError:
                p = 0
            data.append(p)
            

        apNames = None
        if len(stats) > 0:
            apNames = []
            for i in stats.keys():
                apNames.append(i)
                data.append(stats[i])

        if apNames != None:
            self.sheet.get_worksheet(1).update(f"{chr(ord('A') + len(listedPlayers) + 1)}1", [apNames])
        self.sheet.get_worksheet(1).update(f"A{gp + 2}", [data])

if __name__ == '__main__':
    s = Sheet()
    s.addPointStats("10/24/23")