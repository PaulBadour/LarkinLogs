from PyPDF2 import PdfReader

def getSchedule():
    reader = PdfReader('Schedule.pdf')

    games = []
    info = reader.pages[21].extract_text().split('\n')[1:]

    # Info should have date, time, team against
    # Should also maybe iterate twice since each line has 2 games?
    # This might also be something that only needs to be ran once and made into a csv file
    for i in info:
        #input(i)
        g = {}


if __name__ == "__main__":
    print(getSchedule())