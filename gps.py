import time
import serial
import string
import pynmea2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO direction (IN / OUT)
GPIO.setup(21, GPIO.IN)


#setup the serial port to which GPS is connected to
port = "/dev/ttyAMA0"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)
dataout  = pynmea2.NMEAStreamReader()

def email():
    fromaddr = "alina.jones.037@gmail.com"
    toaddr = "akashshingha850@gmail.com"
     
    msg = MIMEMultipart()
     
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "He is in trouble"
     
    body = "I am in trouble. Please help me. My location is http://maps.google.com/maps?q=" + lat + "," + lon"
     
    msg.attach(MIMEText(body, 'plain'))
     
    #filename = "NAME OF THE FILE WITH ITS EXTENSION"
    #attachment = open("PATH OF THE FILE", "rb")
     
    #part = MIMEBase('application', 'octet-stream')
    #part.set_payload((attachment).read())
    #encoders.encode_base64(part)
    #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    #msg.attach(part)
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "alina420")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

while True:
    newdata = ser.readline()
    print ("getting new lat")
    if newdata[0:6] == '$GPGGA':
        newmsg = pynmea2.parse(newdata)
        newlat = newmsg.latitude
        print(newlat)
        newlong = newmsg.longitude
        print(newlong)
        lat  = str(newlat)
        lon = str(newlong)
        
            try:
                print ("Sending mail")
                email()
                print ("Mail Sent")
            except:
                print("error, couldnt send mail, be sure to enable non secure apps login on sender's email")

            time.sleep(3)
