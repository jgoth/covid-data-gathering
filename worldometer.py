import json
from io import StringIO
import requests
from lxml import etree
url = "https://www.worldometers.info/coronavirus"
response = requests.get(url)

parser = etree.HTMLParser()
tree = etree.parse(StringIO(response.text), parser)
start_table = False
TABLE_ID_COUNTRIES_TODAY = "main_table_countries_today"
TABLE_ID_COUNTRIES_YESTERDAY = "main_table_countries_yesterday"
id_search = TABLE_ID_COUNTRIES_YESTERDAY
find_table_rows = '//table[@id="' + id_search + '"]/tbody/tr/td/a[@class="mt_a"]'
cells = tree.xpath(find_table_rows)

records = []
for cell in cells:
    if cell.text is not None:
        print("Cell: " + cell.text)
    country = cell.text

    index = 0
    for sibling in cell.itersiblings():
        print(sibling.text)
        index += 1
    index = 1
    record = {}
    record['country'] = country
    for sibling in cell.getparent().itersiblings():
        switcher = {
            0: "country",
            1: "total-cases",
            2: "new-cases",
            3: "total-deaths",
            4: "new-deaths",
            5: "total-recovered",
            6: "active-cases",
            7: "serious-critical",
            8: "cases-1m-pop",
            9: "deaths-1m-pop",
            10: "total-tests",
            11: "total-1m-pop",
            12: "population"
        }
        key = switcher.get(index, None)
        if key is not None:
            record[key] = sibling.text
        else:
            print(str(index) + " has no key")
        index += 1
    records.append(record)
    #print()
print(json.dumps(records, indent=4))
#for record in records:

exit(1)



def is_country(cell):
    children = cell.getchildren()
    if children is not None and len(children) > 0:
        return children[0].text
    return None
#print(soup.prettify())