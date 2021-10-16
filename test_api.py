from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'tokens.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1Fzhkd4fhKD8ux-Ocv5oXXix_e7wd--7Yweorum8YkI0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

# пример
def get_listID():
    sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    properties = sheet_metadata.get('sheets')
    for  item in properties:

        if item.get("properties").get('title') == 'SHEET_TITILE':
            print( item.get("properties").get('sheetId')) 
         

   


# print(get_listID())



# Пример чтения таблицы 
def read_sheet(list_name: str, range_of_list: str):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"'{list_name}'!"+f'{range_of_list}', # 'A1:E10'
        majorDimension='COLUMNS'
    ).execute()
    return values
# print(read_sheet('921704-2021','A1:E10'))  
# Пример создания листа
def create_list_sheet(year: str):
    results = service.spreadsheets().batchUpdate(
    spreadsheetId = spreadsheet_id,
    body = 
    {
    "requests": [
        {
        "addSheet": {
            "properties": {
            "title": "921704-"+year,
            "gridProperties": {
                "rowCount": 40,
                "columnCount": 12
            }
            }
        }
        }
    ]
    }).execute()

# create_list_sheet('2022')

# Пример записи в файл
values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "B3:C4",
             "majorDimension": "ROWS",
             "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
            {"range": "D5:E6",
             "majorDimension": "COLUMNS",
             "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
	]
    }
).execute()