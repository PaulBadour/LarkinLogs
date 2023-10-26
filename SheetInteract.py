from GetStats import getOpponent, getPlayerPoints
import gspread
import random as r
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Sheet:
    drafted = set()
    def __init__(self):
        cred = gspread.service_account("cred.json")
        self.sheet = cred.open_by_key('1PhKd7v2ydqVTw3osRN7G9Vtd264ENbLSJ1-46L7yUPA')
        
    def __del__(self):
        self.sheet.client.session.close()


    def setupGame(self, date):
        gp = int(self.sheet.get_worksheet(2).acell('B1').value)
        startCell = (6 * gp) + 4
        
        

        

        #Figuring out pick order
        #Step 1: get last games points
        game = self.sheet.get_worksheet(0)
        refCell = startCell - 6
        lastGamePoints = []
        for i in range(4):
            lastGamePoints.append((game.acell(f'A{refCell + i + 1}').value, game.acell(f'G{refCell + i + 1}').value))

        order = sorted(lastGamePoints, key=lambda x: x[1])
        
        i = 0
        sorts = []
        while i < 3:
            if order[i][1] == order[i + 1][1] and (order[i], order[i + 1]) not in sorts and (order[i + 1], order[i]) not in sorts:
                sorts.append((order[i], order[i + 1]))
                s = self.getTotalScores()
                if s[order[i][0]] > s[order[i + 1][0]]:
                    temp = order[i]
                    order[i] = order[i + 1]
                    order[i + 1] = temp
                    i -= 2

                elif s[order[i][0]] == s[order[i + 1][0]]:
                    print('Coin Flip')
                    if r.randrange(2) == 1:
                        temp = order[i]
                        order[i] = order[i + 1]
                        order[i + 1] = temp
                        i -= 2
            i += 1


        game.update_acell(f'A{startCell}', date)
        game.update_acell(f'B{startCell}', f'v. {getOpponent(date)}')

        for i in range(4):
            game.update_acell(f'A{startCell + i + 1}', order[i][0])
            game.update_acell(f'D{startCell + i + 1}', f'=INDEX(StatDump!A{gp + 2}:Z{gp + 2}, 0, MATCH(LOWER(B{(6*gp)+5 + i}), StatDump!B1:Z1, 0) +1)')
            game.update_acell(f'E{startCell + i + 1}', f'=INDEX(StatDump!A{gp + 2}:Z{gp + 2}, 0, MATCH(LOWER(C{(6*gp)+5 + i}), StatDump!B1:Z1, 0) +1)')
            game.update_acell(f'G{startCell + i + 1}', f'=SUM(D{(6*gp) + 5 + i}:E{(6*gp) + 5 + i})')
            


        # This coudl be combined if API space becomes an issue
        self.sheet.get_worksheet(2).update('B1', gp + 1)
        self.sheet.get_worksheet(2).update('B2', order[0][0])
        self.sheet.get_worksheet(2).update('B3', order[1][0])
        self.sheet.get_worksheet(2).update('B4', order[2][0])
        self.sheet.get_worksheet(2).update('B5', order[3][0])
        self.sheet.get_worksheet(2).update('B6', 0)
        self.sheet.get_worksheet(2).update('B7', startCell)



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

    def startDraft(self):
        self.sheet.get_worksheet(2).update('B6', 1)
        self.sheet.get_worksheet(2).update('B8', '')
        return self.sheet.get_worksheet(2).acell('B2').value

    def getTotalScores(self):
        game = self.sheet.get_worksheet(0)
        scores = {}
        scores['Eddy'] = int(game.acell('K5').value)
        scores['Paul'] = int(game.acell('K6').value)
        scores['Flynn'] = int(game.acell('K7').value)
        scores['Johnson'] = int(game.acell('K8').value)
        return scores

    def getNextDraftee(self):
        pickNum = int(self.sheet.get_worksheet(2).acell('B6').value)
        if pickNum == 0:
            return None
        if pickNum > 4:
            pickNum = (pickNum * -1) + 9
        return self.sheet.get_worksheet(2).acell(f'B{1 + pickNum}').value
    

    def pickPlayer(self, player):
        drafted = self.sheet.get_worksheet(2).acell('B8').value
        drafted = drafted.split(' ') if drafted != None else []
        if player in drafted:
            return False
        
        drafted.append(player)
        pick = int(self.sheet.get_worksheet(2).acell('B6').value)
        refCell = int(self.sheet.get_worksheet(2).acell('B7').value)
        if pick < 5:
            self.sheet.get_worksheet(0).update(f'B{refCell + pick}', player)
        else:
            self.sheet.get_worksheet(0).update(f'C{refCell + (pick * -1) + 9}', player)
        
        if pick < 8:
            self.sheet.get_worksheet(2).update('B8', ' '.join(drafted))
            self.sheet.get_worksheet(2).update('B6', pick + 1)
        else:
            self.sheet.get_worksheet(2).update('B6', 0)
            return None
        return True
        

if __name__ == '__main__':
    s = Sheet()
    s.setupGame("10/26/23")