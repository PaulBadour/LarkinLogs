import gspread

cred = gspread.service_account("credentials.json")
sheet = gc.open_by_key('1PhKd7v2ydqVTw3osRN7G9Vtd264ENbLSJ1-46L7yUPA')
print(sheet.title)
