from flask import Flask
from flask import request
from flask import escape
from flask import render_template
from script import *

app = Flask(__name__, static_folder="C:\\Users\\KIIT\\Desktop\\Final\\static")

valDict = {'dob' : '','first_name' : '', 'last_name' : '', 'email' : '', 'phone_number' : '',
        'gender' : '' ,'address' : '','city' : '','region' : '','postal' : '' ,
         'vidPath' : '', 'country' : '','vidTime' : '','illness' : '','misc_msg' : ''}
vidTime = 10
#addr = "C:\\Users\\KIIT\\Desktop\\Major Project\\Flask\\Repos\\test14.mp4"
@app.route("/")
def index():
    valDict['first_name'] = str(escape(request.args.get('first_name', '')))
    valDict['last_name'] = str(escape(request.args.get('last_name', '')))
    valDict['email'] = str(escape(request.args.get('email', '')))
    valDict['phone_number'] = str(escape(request.args.get('phone_number', '')))
    valDict['address'] = str(escape(request.args.get('address', '')))
    valDict['city'] = str(escape(request.args.get('city', '')))
    valDict['region'] = str(escape(request.args.get('region', '')))
    valDict['postal'] = str(escape(request.args.get('postal', '')))
    valDict['country'] = str(escape(request.args.get('country', '')))
    valDict['illness'] = str(escape(request.args.get('illness', '')))
    valDict['misc_msg'] = str(escape(request.args.get('misc_msg', '')))
    valDict['dob'] = str(escape(request.args.get('dob', '')))
    valDict['gender'] = str(escape(request.args.get('gender', '')))
    valDict['vidPath'] = str(escape(request.args.get('vidPath', '')))
    global vidTime
    return render_template("index.html")

@app.route("/user")
def user():
    hrm = hrtRate(valDict['vidPath'],vidTime)
    return render_template("user.html",name=valDict['first_name'], dob=valDict['dob'], 
    gender = valDict['gender'], email = valDict['email'], phone_number = valDict['phone_number'], 
    address = valDict['address'], city = valDict['city'], region = valDict['region'],
    postal = valDict['postal'], country = valDict['country'], illness = valDict['illness'],
    misc_msg = valDict['misc_msg'], vidTime = vidTime, heartRate = hrm)


if __name__ == "__main__":
    app.run(debug=False)