import requests
from bs4 import BeautifulSoup as bs

# Should probably make this in some better way
GOALIES = ('Ville Husso', 'James Reimer')
DEFENSE = ('Jake Walman', 'Moritz Seider', 'Ben Chiarot', 'Justin Holl', 'Shayne Gostisbehere', 'Olli Maatta', 'Jeff Petry')

def getPlayerPoints(gameDate):
    OT = False
    URL = "https://www.statmuse.com/nhl/ask?q=player+stats+red+wings+" + gameDate
    page = requests.get(URL)
    soup = bs(page.content, 'html.parser')

    points = {}
    
    for i in soup.find_all('tr')[1:]:
        p = 0
        # This is a fucking mess but it works, i am not good at web scraping
        name = i.contents[0].contents[-1].contents[-1].contents[-1]
        if name not in GOALIES:
            goals = int(i.contents[5].contents[0].contents[0])
            assists = int(i.contents[6].contents[0].contents[0])
            p += assists
            if name in DEFENSE:
                p += 3*goals
            else:
                p += 2*goals
            # ADD OT SHIT
        else:
            newReq = requests.get('https://www.statmuse.com/nhl/ask?q={}+save+pct+{}'.format(name.replace(' ', '+'), gameDate))
            newSoup = bs(newReq.content, 'html.parser')
            save = float(newSoup.find_all('tr')[1].contents[2].contents[0].contents[0])
            if save >= .90 and save < .92:
                p = 1
            elif save >= .92 and save < .94:
                p = 2
            elif save >= .94 and save < 1:
                p = 3
            elif save == 1.0:
                p = 5

        points[name] = p
    
    # Now for wings score
    page = requests.get('https://www.statmuse.com/nhl/ask?q=red+wings+score+' + gameDate)
    soup = bs(page.content, 'html.parser')

    scores = {}

    teamOne = soup.body.contents[2].contents[0].contents[2].contents[0].contents[1].contents[0].contents[0]
    teamTwo = soup.body.contents[2].contents[0].contents[2].contents[0].contents[2].contents[0].contents[0]
    other = teamOne if teamOne != 'DET' else teamTwo

    scores[teamOne] = int(soup.body.contents[2].contents[0].contents[2].contents[5 if OT else 4].contents[1].contents[0])
    scores[teamTwo] = int(soup.body.contents[2].contents[0].contents[2].contents[5 if OT else 4].contents[2].contents[0])
    
    p = scores['DET'] - scores[other] - 1
    if p < 0:
        p = 0
    
    points["Wings"] = p

    return points

if __name__ == '__main__':
    for i,j in getPlayerPoints("10/22/23").items():
        print(i, j)