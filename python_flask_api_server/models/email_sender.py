from typing import List
from flask import Flask, request
import smtplib
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def Send_Admin_Support_Email():    
    _result = request.get_json()
    msgTitle = _result["msgTitle"]
    msg = _result["msg"]
    email = str(_result["email"]).split(",")
    message = msg

    return Send_Email(email, message, msgTitle)
    # {"message": "Email Sent Successfully"}


def Send_Guest_To_Support_Email():    
    _result = request.get_json()
    msgTitle = _result["msgTitle"]
    msg = _result["msg"]
    email = _result["email"]
    message = "<b>Sender:</b> " + email + "<br />" + \
        "<b>Message:</b> <br />" + msg

    Send_Email(f"support@{config('domain_base')}", message, msgTitle)

    message = "Hi, below is a copy of your message which we recieved.<br />" + \
        "Our staff will get back to you shortly.<br /><br />" + msg
    return Send_Email(email, message, "Re: " + msgTitle)


def Send_Email(receivers, message_content, title):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = f'support@{config("domain_base")}'
    msg['To'] = receivers
    message_content += f"""
        <br /><br />
        Regards,<br />
        {config("domain_base")}
        <br />"The {config('comp_name')}  team.
    """
    body = MIMEText(message_content, 'html')
    msg.attach(body)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(f"support@{config('domain_base')}", receivers, msg.as_string())
        smtpObj.quit()      
        return {"message": "Successfully sent email"}
    except smtplib.SMTPException:
        return {"message": "Error: unable to send email"}
