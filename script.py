#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import string
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import csv
import config

def send_mail(vorname, nachname, email, password, username):
    sender = 'support@juniter.de'
    receiver = email
    
    username = username.encode('utf8') + '@cct-ev.de'
    text="""
    <html>
  <head></head>
  <body>
    Hallo %(vorname)s %(nachname)s,<br />

<p>auch wir von Juniter möchten dich noch einmal ganz herzlich im Verein
begrüßen. Dir wurde jetzt ein CCT-Benutzeraccount angelegt, mit dem
du vollen Zugriff auf sämtliche internen IT-Dienste des Vereins bekommst.</p>

<p>Dein Benutzername ist:

<pre>%(username)s</pre> </p>

<p>Dein vorläufiges Passwort ist:

<pre>%(password)s</pre></p>

<p>Als nächsten Schritt solltest du dich unter https://webmail.all-inkl.com
einloggen und dein Passwort unter Einstellungen ändern. Dies
dient der Sicherheit deines Accounts und ist außerdem notwendig, um einige
Funktionen deines Accounts (inklusive des Wissensmanagementsystems!)
endgültig freizuschalten. Logge dich danach auf den internen Seiten aus
und wieder ein, um die Passwortänderung zu übernehmen.</p>

<p>Um unsere IT-Systeme gut nutzen zu können, ist es wichtig, dass Du ihre
Funktionalität kennst. Nimm Dir bitte etwas Zeit und blättere durch die
Anleitungen, die im Wissensmanagement liegen: http://wms.cct-ev.de >
IT-Dokumentation (der Button oben in der Mitte). Dort findest Du neben
bebilderten Schritt-für-Schritt-Anleitungen auch kurze Videodokumentationen
zur Einrichtung der wichtigsten Systeme auf Deinem Computer, also z.B.
E-Mail und Zugriff auf CCT-Daten.</p>

<p>Bei technischen Problemen, z.B. dem Ausfall eines Systems, schreibe bitte
ein Ticket im Verfolgungssystem unter <br/>

https://redmine.cct-ev.de/projects/it-support

oder in ganz schlimmen Fällen (z.B. bei nicht-funktionierendem Login) eine
E-Mail an support@juniter.de</p>

<p>Viel Erfolg auf deinem weiteren Weg im Verein,<br/>
dein Team Juniter</p>
      </body>
</html>""" %{"vorname":vorname, "nachname":nachname, "username":username, "password":password}

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Willkommen im CCT!"
    msg['From'] = sender
    msg['To'] = receiver
    part1 = MIMEText(text, 'html')
    msg.attach(part1)
    s = smtplib.SMTP('w013d91b.kasserver.com')
    s.login('info@service-cct.de',config.email_pw)
    s.sendmail(sender, receiver, msg.as_string())



def id_generator(size=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_user(output):
    file = open('output.txt','w+')
    table = {
        ord(u'ä'): u'ae',
        ord(u'ö'): u'oe',
        ord(u'ü'): u'ue',
            ord(u'ß'): u'ss',
    }    
    driver = webdriver.Firefox()
    driver.get("http://kas.all-inkl.com")
    wait = WebDriverWait(driver,10)
    try:
        input = wait.until(EC.presence_of_element_located((By.ID, "loginname")))
        password = wait.until(EC.presence_of_element_located((By.ID, "passwort")))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][value='english']"))).click()

        #username and password have to come from a config file
        input.send_keys(config.allinkl_username)
        password.send_keys(config.allinkl_pw)
        password.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Email"))).click()
        for interessent in output:
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Email Account"))).click()
            wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Create new mail account"))).click()

            vorname = interessent[0]
            vorname = vorname.replace(" ", ".")
            nachname = interessent[1]
            nachname = nachname.replace(" ",".")

            email = interessent[2]           
            mail = wait.until(EC.presence_of_element_located((By.NAME, "mail")))
            username = vorname.lower().decode('utf8').translate(table)+ "." + nachname.lower().decode('utf8').translate(table)
            
            mail.send_keys(username)

            user_pw = id_generator()

            pw1 = wait.until(EC.presence_of_element_located((By.ID, "pwfeld_1")))
            pw2 = wait.until(EC.presence_of_element_located((By.ID, "pwfeld_2")))

            pw1.send_keys(user_pw)
            pw2.send_keys(user_pw)
            domain = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "domain")))
            select = Select(domain)
            select.select_by_visible_text("cct-ev.de")
            wait.until(EC.presence_of_element_located((By.ID, "show_password_yes"))).click()
            wait.until(EC.presence_of_element_located((By.NAME, "button1"))).click()
            send_mail(vorname, nachname, email, user_pw, username)
            file.write(username+'@cct-ev.de\n')
            print username + ' erstellt mit pw ' + user_pw
            time.sleep(3)
    finally:
        driver.close()
        file.close()
        #return user_pw, mailname
        print 'Alle User erstellt'
        
  
def readFile(filename):
     output =[]
     with open(filename) as csvfile:
         reader = csv.reader(csvfile)
         for row in reader:
            output.append(row)
     return output

#main()
output = readFile('interessenten.csv')
generate_user(output)
