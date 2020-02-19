import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'immunizationcompliance@gmail.com'
PASSWORD = 'Comp129!'

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main(patients):
    names = patients[0]
    emails = patients[1]
    alertNums = patients[2]
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email, alertNum in zip(names, emails, alertNums):
        
        emailFile = "email_template_" + str(alertNum) + ".txt"
        message_template = read_template(emailFile)
        
        msg = MIMEMultipart()       # create a message
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Immunization"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
    
if __name__ == '__main__':
    #main((["Jason", "Daniel"], ["j_vanbladel@u.pacific.edu", "d_adler@u.pacific.edu"], [1,2]))
