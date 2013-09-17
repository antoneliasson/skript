#!/usr/bin/env python3
"""
IP Monitor

Sends an e-mail if the network's external IP address has changed since last run.

SMTP credentials are read from the user's ~/.netrc file. It expects an entry like this:

    machine smtp.example.com
    login johndoe@example.com
    password supersecret

where `machine` matches the `smtp_address` below and `login` is typically your
e-mail address with or without the domain depending on your SMTP server.

Typically, this program is run as a cron job by a crontab entry like this:

    0 */12 * * * ~/bin/ipmonitor.py

(Every day, at 0:00 and 12:00 in this example)

"""

# Configuration
smtp_address = 'mail.antoneliasson.se'
sender_address = 'relay@antoneliasson.se' # E-mail 'From' field
recipient_address = 'info@antoneliasson.se' # E-mail 'To' field

import urllib.request
import re
import os.path

from email.mime.text import MIMEText
from email.utils import formatdate

from netrc import netrc
from smtplib import SMTP

def get_ip():
    with urllib.request.urlopen('http://dns.loopia.se/checkip/checkip.php') as f:
        html = f.read().decode('utf-8')
        ip = re.findall('[0-9]+.[0-9]+.[0-9]+.[0-9]+', html)[0]
    
    return ip

def compare(ip):
    home = os.path.expanduser("~")
    try:
        file = open(home + '/.ipmonitor', 'r')
        return file.read() == ip
    except IOError as e:
        return False

def update(ip):
    home = os.path.expanduser("~")
    try:
        file = open(home + '/.ipmonitor', 'w')
        file.write(ip)
        return True
    except IOError as e:
        return False

def compose(ip, wrote, sender, recipient):
    msg = MIMEText('')
    if wrote:
        msg.set_payload('New IP address: %s.' % ip)
    else:
        msg.set_payload('New IP address: %s.\n\nUnable to create config file!' % ip)
    msg['Subject'] = 'IP address change: %s' % ip
    msg['From'] = sender
    msg['To'] = recipient
    # RFC 2822, section 3.3: "The date and time-of-day SHOULD express local time."
    # Anton: "Use UTC and the world will be a better place."
    msg['Date'] = formatdate(localtime = False)
    
    return msg

def send(msg, server, port):
    username, _, password = netrc().authenticators(server)
    
    smtp = SMTP(server, port)
    smtp.starttls()
    smtp.login(username, password)
    smtp.send_message(msg) # Python >= 3.2
    # smtp.sendmail(msg['From'], msg['To'], str(msg)) # Python >= 3.1
    smtp.quit()

def main():
    ip = get_ip()
    if not compare(ip):
        print('New IP: %s' % ip)
        wrote = update(ip)
        if wrote:
            print('Wrote config')
        else:
            print('Failed to write config')
        msg = compose(ip, wrote, sender_address, recipient_address)
        send(msg, smtp_address, 587)
        print('Sent e-mail')

if __name__ == '__main__':
    main()
