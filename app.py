from flask import Flask, render_template, request
import sqlite3
import datetime
import requests
import json
import pytz

app=Flask(__name__)

class MyError(Exception):    
    def __init__(self, value):  
        self.value = value  
      
    def __str__(self):  
        return(repr(self.value))

def current_time():
    local_tz = pytz.timezone("Asia/Kolkata")
    return datetime.datetime.now(tz=local_tz)

def store_data(val):
    mydb = sqlite3.connect('data.sqlite')
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS data(fname TEXT, sname TEXT, time TEXT, device TEXT, result TEXT)")
    mydb.commit()
    sql = "INSERT OR IGNORE INTO data (fname, sname, time, device, result) VALUES (?, ?, ?, ?, ?)"
    mycursor.execute(sql,val)
    mydb.commit()
            
url = "https://love-calculator.p.rapidapi.com/getPercentage"

headers = {
    'x-rapidapi-host': "love-calculator.p.rapidapi.com",
    'x-rapidapi-key': "cd484d0234msheee09c971fa1b4cp154e0ejsna5da5f9b640e"
    }


@app.route("/", methods=["GET","POST"])
def index():
    try:
        fname = str(request.form.get("fname"))
        sname = str(request.form.get("sname"))
        if(fname==''):
            raise MyError("Please enter your name.")
        if(sname==''):
            raise MyError("Please enter your partner/lover/crush Name.")
        if(fname==str(None)):
            raise Exception(ValueError)
        querystring = {"fname":fname,"sname":sname}
        response = requests.request("GET", url, headers=headers, params=querystring)
        
        if response.status_code != 200:
            result='ERROR: API request unsuccessful'
        else:
            time=str(current_time())
            device = str(request.headers)
            device=device.strip()
            data=json.loads(response.text)
            result=data['percentage']+"% "+ data['result']
            val = (fname, sname, time, device, result)
            store_data(val)

    except MyError as error:
        result=error
    
    except:
        result=''
    return render_template("index.html", result=result)

if __name__=="__main__":
    app.run()
