import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time, os

print("Authenticating...")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# Create a service account for a google cloud project with the Google Drive and Google Sheets APIs enabled and save its credentials as service_account_credentials.json
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json', scope)
client = gspread.authorize(creds)

print("Authenticated")

sfile = open("service.run","w")
sfile.write("Delete this file to stop the sync service.")
sfile.close()

print("Service file created")

while os.path.exists('service.run'):
    print("Fetching scores...")
    try:
        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        sheet = client.open("Leaderboard").sheet1
        # Extract and print all of the values
        records = sheet.get_all_records()
        xmldata = "<rows>"
        for record in records:
            d_keys = list(record.keys())
            name = record[d_keys[0]]
            value = record[d_keys[1]]
            color = record[d_keys[2]]
            xmldata += "<row>"
            xmldata += "<name>" + str(name) + "</name>"
            xmldata += "<value>" + str(value) + "</value>"
            xmldata += "<color>" + str(color) + "</color>"
            xmldata += "</row>"
        xmldata += "</rows>"
        xmlfile = open("scores.xml","w")
        xmlfile.write(xmldata)
        xmlfile.close()
    except Exception as ex:
        print("An error occurred: " + str(ex))
    print("Sleeping...")
    time.sleep(30)
