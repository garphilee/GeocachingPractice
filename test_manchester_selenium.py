import re
from selenium import webdriver # browser to obtain dynamic html by executing javascript
from selenium.webdriver.chrome.options import Options
import xlsxwriter # write .xlsx spreadsheet

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = r'C:\Users\garph\OneDrive\Documents\coding projects\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://manchesterorchestra.com/') # opens browser to (url)

#print('driver page_source:', driver.page_source)
page_source = driver.page_source

driver.quit() # closes browser

print(page_source) # check html

# step 2: now, isolate locations
pattern2 = r'seated-event-venue-location.>(.*)<' # grab location data
locations = re.findall(pattern2, page_source) # save locations in list
print('locations:',locations) # check location list

# step 3: write location to spreadsheet (.xlsx)
workbook = xlsxwriter.Workbook(r'C:\Users\garph\OneDrive\Documents\coding projects\test_manchester\test_manchester.xlsx') # creates .xlsx file with name and in path
worksheet = workbook.add_worksheet() # creates worksheet

# Write columns
worksheet.write(0, 1, "locations")
worksheet.write(0, 0, "order")

# Iterate over the data and write it out row by row.
for i in locations: # (row, column, data)
    worksheet.write(locations.index(i)+1, 0, locations.index(i)+1)
    worksheet.write(locations.index(i)+1, 1, i)

workbook.close() # save and close workbook
