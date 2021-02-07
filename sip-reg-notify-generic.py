import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pprint import pprint
from netmiko import ConnectHandler


## Email Details ##
port = 465  # For SSL
sender_email = "****"
receiver_email = "****"
password = "*****"

## CUBE Details ###
router = {"device_type": "cisco_ios","host": "*****", "user": "admin", "pass":"*****"}
trunkname = "******"
####

# Create a secure SSL context
context = ssl.create_default_context()
def sendemail(sender_email,password,receiver_email,body):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        message = MIMEMultipart("alternative")
        message["Subject"] = "Sip Registeration Notification for " + trunkname
        message["From"] = sender_email
        message["To"] = receiver_email
        # Create the plain-text and HTML version of your message
        text = body
        html = body

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        server.sendmail(sender_email,receiver_email,message.as_string())
        #print(message)

# Send email here


net_connect = ConnectHandler(ip=router["host"],username=router["user"],password=router["pass"],device_type=router["device_type"])
send_cli = net_connect.send_command("show sip-ua register status")
send_cli = send_cli.split()
regiter_status = send_cli[send_cli.index(trunkname)+3]
if regiter_status == 'no':
    body = """\
    <html>
      <body>
       <p>Hi,<br>"""+trunkname+"""@"""+router["host"]+""" SIP trunk is not registreded anymore please contact your system administrtor.<br>
      </p>
     </body>
    </html>
    """
    sendemail(sender_email,password,receiver_email,body)