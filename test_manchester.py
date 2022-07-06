import requests
import re
import csv
import xlwt
from xlwt import Workbook
import xlsxwriter # https://xlsxwriter.readthedocs.io/tutorial01.html
from pyexcel_ods import save_data

url = 'https://manchesterorchestra.com/'
# Want to scrape music tour location data from site; (Maybe) Use 'requests' to save html file (or whatever it is)
## (done) Use RegEx to isolate location data
### (done) Write location data to spreadsheet/csv - (used xlsxwriter for .xlsx file)
#### (done) Upload spreadsheet of location data to Google Maps to create custom map of tour venue locations

txt = 'test_manchester.txt' # scraped html should be written to this text file
file = open(txt) # 'r' for read, which is default if left empty
cont = file.read() # reads contents of file
print(cont)

"""  # data might look something like this:
<div class="seated-event-row">
      <div class="seated-event-description-cells">
        <div class="seated-event-date-cell">
          Oct 29, 2022
<!---->        </div>
        <div class="seated-event-venue-cell">
          <div class="seated-event-venue-name">When We Were Young</div>
          <div class="seated-event-venue-location">Las Vegas, NV</div>
        </div>
        <div class="seated-event-details-cell">
            <span class="seated-event-details-sold-out">
              Sold Out
            </span>

        </div>
      </div>
      <div class="seated-event-link-cells">
<!---->        <div class="seated-event-link-cell1">
          <a class="seated-event-link1 seated-event-link1-find-tickets" href="https://link.seated.com/dda310ad-31fd-4180-bb54-2b9e5f5109f3" target="_blank">
<!---->              Join Waitlist
<!---->          </a>
        </div>
      </div>
    </div>
"""

#pattern = r'seated-event-venue-name'
pattern2 = r'seated-event-venue-location.>(.*)<' # grab location data

"""if re.findall(pattern,cont):
    print(len(re.findall(pattern,cont)))
else:
    print('No Match')"""

locations = re.findall(pattern2,cont)

file.close()

print('locations:',locations)

""" <1. Writing to .CSV File>
# write location data to csv to upload to Google Maps
file = open('test_manchester_location.csv','w')
writer = csv.writer(file, dialect='excel')
for i in locations:
    print(i)
    writer.writerow(i)
file.close()
"""

"""# <2. Writing to Spreadsheet .xls file>

# Create Workbook
wb = xlwt.Workbook()

# add_sheet is used to create sheet.
sheet1 = wb.add_sheet('Sheet 1')

# create spreadsheet headers
sheet1.write(0,0,'order')
sheet1.write(1,0,'location')

# add row data
for i in locations:
    print(locations.index(i)+1,":",i)
    sheet1.write(0,locations.index(i)+1,i)

wb.save('example.xls')
"""
"""# <3. Write to .ods file>

data = OrderedDict()
data.update({"Sheet1": [[1,2,3],[4,5,6]]})
data.update({"Sheet 2": [["row 1","row 2","row 3"]]})
save_data("test_manchester.ods", data)
"""

# <4. Write to .xlsx file>
workbook = xlsxwriter.Workbook("test_manchester.xlsx")
worksheet = workbook.add_worksheet()

"""# Some data we want to write to the worksheet.
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)"""

"""# (only used in tutorial example) Start from the first cell. Rows and columns are zero indexed.
row = 0
col = 0"""

# Write columns
worksheet.write(0, 1, "locations")
worksheet.write(0, 0, "order")

# Iterate over the data and write it out row by row.
for i in locations:
    worksheet.write(locations.index(i)+1, 0, locations.index(i)+1)
    worksheet.write(locations.index(i)+1, 1, i)


"""# Write a total using a formula.
worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')"""

workbook.close()
