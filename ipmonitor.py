#!/usr/bin/env python3
"""
IP Monitor

version 1

Sends an e-mail if the network's external IP address has changed since last run.
"""

def get_ip():
    import urllib.request
    import re

    with urllib.request.urlopen('http://dns.loopia.se/checkip/checkip.php') as f:
        html = f.read().decode('utf-8')
        ip = re.findall('[0-9]+.[0-9]+.[0-9]+.[0-9]+', html)[0]
    
    return ip

def compare(ip):
    from os.path import expanduser
    home = expanduser("~")
    try:
        file = open(home + '/.ipmonitor', 'r')
        return file.read() == ip
    except IOError as e:
        return False

def update(ip):
    from os.path import expanduser
    home = expanduser("~")
    try:
        file = open(home + '/.ipmonitor', 'w')
        file.write(ip)
        return True
    except IOError as e:
        return False

def compose(ip, wrote, poster, recipient):
    from email.mime.text import MIMEText
    from email.utils import formatdate
    
    msg = MIMEText('')
    if wrote:
        msg.set_payload('New IP address: %s.' % ip)
    else:
        msg.set_payload('New IP address: %s.\n\nUnable to create config file!' % ip)
    msg['Subject'] = 'IP address change: %s' % ip
    msg['From'] = poster
    msg['To'] = recipient
    # RFC 2822: "Use local time". Anton: "Use UTC".
    msg['Date'] = formatdate(localtime = False)
    
    return msg

def send(msg, server, port):
    from netrc import netrc
    from smtplib import SMTP
    
    username, _, password = netrc().authenticators(server)
    
    smtp = SMTP(server, port)
    smtp.starttls()
    smtp.login(username, password)
    # smtp.send_message(msg) # Python 3.2
    smtp.sendmail(msg['From'], msg['To'], str(msg)) # Python 3.1
    smtp.quit()

def main():
    ip = get_ip()
    if compare(ip):
        pass
#        print('No change')
    else:
        print('New IP: %s' % ip)
        wrote = update(ip)
        if wrote:
            print('Wrote config')
        else:
            print('Failed to write config')
        msg = compose(ip, wrote, 'relay@antoneliasson.se', 'info@antoneliasson.se')
        send(msg, 'mail.antoneliasson.se', 587)
        print('Sent e-mail')

if __name__ == '__main__':
    main()
