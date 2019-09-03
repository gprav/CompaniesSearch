import sqlite3
import datetime
import re

def check_postcode(postcode):
    valid_postcode = False
    postcode = postcode.upper()
    if re.match("^[A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}$", postcode):
        valid_postcode = True
    return valid_postcode

def correct_format(postcode):
    postcode = postcode.upper()
    
    if " " in postcode:
        pass
    else:
        postcode = postcode[0:len(postcode)-3]+" "+postcode[len(postcode)-3:len(postcode)]
    return postcode

def search(postcode):
    current_month = datetime.date.today().replace(day=1)
    previous_month = current_month - datetime.timedelta(days=1)
    str_previous_month = previous_month.strftime("/%m/%Y")
    previous_month2 = previous_month.replace(day=1) - datetime.timedelta(days=1)
    str_previous_month2 = previous_month2.strftime("/%m/%Y")
    previous_month3 = previous_month2.replace(day=1) - datetime.timedelta(days=1)
    str_previous_month3 = previous_month3.strftime("/%m/%Y")
    
    if len(postcode) == 7:
        letter = 3
    else:
        letter = 4
    
    con = sqlite3.connect("Companies.sqlite")
    cur = con.cursor()
       
    sql = "SELECT * FROM t WHERE PostCode LIKE '" + postcode[0:letter] + " %'"
    sql += "AND (IncorporationDate LIKE '%" +str_previous_month+"' OR IncorporationDate LIKE '%"+str_previous_month2
    sql +="' OR IncorporationDate LIKE '%"+str_previous_month3+"')"
    cur.execute(sql)
        
    rows = cur.fetchall()
    
    con.commit()
    con.close()
    
    return rows, previous_month3, previous_month

if __name__ == "__main__":
    postcode = input("Enter postcode: ")
    valid_postcode = False
    while valid_postcode == False:
        valid_postcode = check_postcode(postcode)
        if valid_postcode == False:
            postcode = input("Invalid Postcode. Enter postcode again: ")
    postcode = correct_format(postcode)
    print(postcode) 
    rows, previous_month3, previous_month = search(postcode)
    for row in rows:
        print(row)
    