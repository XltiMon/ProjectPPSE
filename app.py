from flask import Flask,render_template, request, session
from flask import jsonify,abort,redirect
import os
from waitress import serve
import xml.etree.cElementTree as ET
from flask import send_file, send_from_directory
from xml.etree.ElementTree import parse
import sqlite3
from flask_mail import Mail, Message 


app = Flask(__name__)
mail = Mail(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'projectpositiveselfesteem@gmail.com'
app.config['MAIL_PASSWORD'] = 'ppse2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 






@app.errorhandler(404) 
def not_found(e): 
  return render_template("errorpages/error404.html"),400

@app.errorhandler(500)
def internal_error(e):
  return render_template('errorpages/error500.html'), 500

@app.errorhandler(410)
def gone(e):
  return render_template("errorpages/error410.html"),410



def handleemail(name,email,type):
    with open(type+".list", "a") as email_list:
      email_list.write("USERNAME: "+name+" USEREMAIL: "+email+"\n")
    
    
def mailout(email,name,template):
   msg = Message('Project Positive Self-Esteem - Getting Started!',cc=["yusuf@yusufdogan.online"],sender = "projectpositiveselfesteem@gmail.com", recipients = [email])
   msg.html = open(template).read()
   mail.send(msg)

   return "Sent"

@app.route("/sitemap.xml")
def getmap():
    return send_from_directory('templates', "sitemap.xml")

@app.route("/robots.txt")
def getrobots():
    return send_from_directory('templates', "robots.txt")


##def track_visitor():
##  
##  ip_address = request.remote_addr
##  isfrominsta = request.args.get('forward')
##  requestdatetime = datetime.now()
##    
##  print(ip_address)
##  ipmainurl = "http://ip-api.com/xml/{0}?fields=status,message,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,mobile,query".format(ip_address)
##  
##  with urllib.request.urlopen(ipmainurl) as xmlurl:
##    tree = ET.ElementTree(file=xmlurl)
##    root =  tree.getroot()
##
##  
##    country = root.findtext('country')
##    region = root.findtext('region')
##    city = root.findtext('city')
##    zipcode  = root.findtext('zip')
##    mobile = root.findtext('mobile')
##    latitude = root.findtext("lat")
##    longitude = root.findtext("lon")
##
##    conn = sqlite3.connect('VisitorInformation.db')
##    cursor = conn.cursor()
##    
##    params = (country,region,city,zipcode,mobile,isfrominsta,requestdatetime,ip_address,latitude,longitude,1)
##    conn.execute("INSERT INTO VistorInformation (Country,Region,City,Zip,Mobile,Instagram,FirstVistedDate,IPaddress,Latitude,Longitude,TimesVisted) VALUES (?,?,?,?,?,?,?,?,?,?,?)",params);
##    conn.commit()
##    conn.close()
####
  

@app.before_request
def limit_remote_addr():
    if '98.240.107.60' in request.url_root:
      return redirect("http://www.yusufdogan.online")


@app.route('/submitproject', methods=['POST'])
def submitemail():
     personname = request.form['name']
     email = request.form['email']
     handleemail(personname,email,"emails")
     mailout(email,personname,"mirrormessage.html")
     return render_template('index.html')


##PODCAST
@app.route("/podcast")
def podcastfeed():
  return open("podcastfeed.xml").read()



@app.route("/")
def indexhome():
  return render_template('index.html')

@app.route("/projects")
def sendprojectpage():
   return render_template("projects.html")

@app.route("/mirrormessage")
def routetoevent():
   return render_template("projectmirrormessage.html")

@app.route("/nbcLX")
def NBCInterview():
  return redirect("https://www.lx.com/news/nashville-teen-combating-food-insecurity/20411/")
  

@app.route("/gallery")
def gallery():
  return render_template("galleryindex.html")

@app.route("/r")
def backdoor():
 password = request.args.get('p')
 if password == "onion":
  return redirect("http://myapd.hopto.org:2250/getinstaller")
 else:
  return redirect("http://www.yusufdogan.online")
 return redirect("http://www.yusufdogan.online")

# run the application
if __name__ == "__main__":
##    app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)
