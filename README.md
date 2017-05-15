# create_user_script

This is used for automatically creating Email accounts on http://kas.all-inkl.com

## Requirements
- Selenium 3.4.1
- geckodriver 0.16.0
- Firefox

## Input
A csv file named `interessenten.csv`

The format should be: `first_name,last_name,email_address`

## Output
A `output.txt` file with all the resulting emails for easy copy-pasting into KAS
