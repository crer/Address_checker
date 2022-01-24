import requests
import json, csv
import re
import time


FILE_ID = "1H1a9eBamflt3w-4BPEk1kJYc4VgsDBWlDjkS0hV5tAY"
google_sheet_url = f"https://docs.google.com/feeds/download/spreadsheets/Export?key={FILE_ID}&exportFormat=csv&gid=0"

headers = {'User-Agent': 'Mozilla/5.0'}
usps_url = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"


def check_addresses():
    fields = []

    response = requests.get(google_sheet_url)

    decoded_content = response.content.decode('utf-8')
    data = csv.reader(decoded_content.splitlines(), delimiter=',')

    fields = next(data)
    fields.append('Status')

    with open('output.csv', 'w', encoding='UTF8', newline='') as csvoutput:
        writer = csv.writer(csvoutput)
        writer.writerow(fields)

        for row in data:
            street = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]

            pl = {
                'address1': street,
                'zip': zip_code
                }
            response_post = requests.post(usps_url, headers=headers, data=pl)
            output = eval(response_post.text)

            if output["resultStatus"] == "SUCCESS":
                out = output["addressList"][0]
                if (city == out['city']) and (state == out['state']):
                    row.append("Valid")
                else:
                    row.append("Not Valid 2")
            else:
                row.append("Not Valid")
            time.sleep(2)

            writer.writerow(row)


if __name__ == "__main__":
    check_addresses()




