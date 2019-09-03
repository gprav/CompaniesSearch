from zipfile import ZipFile
import requests
import io
import csv
import os
import sqlite3
import datetime 

def download():
	current_month = datetime.date.today().replace(day=1)
	str_current_month = current_month.strftime("%Y-%m")
	
	file_path = "C:\\Users\\Jibin\\eclipse-workspace\\Companies House\\BasicCompanyDataAsOneFile-"+str_current_month+"-01.csv"
	if os.path.exists(file_path) == False:
		url = "http://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-"+str_current_month+"-01.zip"
		r = requests.get(url)
		z = ZipFile(io.BytesIO(r.content))
		z.extractall()
	
	con = sqlite3.connect("Companies.sqlite")
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS t")
	cur.execute("CREATE TABLE t (CompanyName, AddressLine1, AddressLine2, PostTown, County, Country, PostCode, IncorporationDate);")
	
	filename = "BasicCompanyDataAsOneFile-"+str_current_month+"-01.csv"
	with open(filename, "r", encoding="utf8") as f:
		dr = csv.DictReader(f)
		to_db = [(i['CompanyName'], i['RegAddress.AddressLine1'], i[' RegAddress.AddressLine2'], i['RegAddress.PostTown'], i['RegAddress.County'], i['RegAddress.Country'], i['RegAddress.PostCode'], i['IncorporationDate']) for i in dr]
	
	cur.executemany("INSERT INTO t (CompanyName, AddressLine1, AddressLine2, PostTown, County, Country, PostCode, IncorporationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
	
	con.commit()
	con.close()
	
if __name__ == "__main__":
	download()