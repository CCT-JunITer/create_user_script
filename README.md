# create_user_script

This is used for automatically creating Email accounts on http://kas.all-inkl.com

##Requirements
-Selenium 3.4.1
-geckodriver 0.16.0
-Firefox

You also need a config.py file which includes the allinkl_username, allinkl_pw and the email_pw of info@service-cct.de

##Input
A csv file named interessenten.csv
The format should be: first_name,last_name,email_address

##Output
A output.txt file with all the resulting emails for easy copy-pasting into KAS
