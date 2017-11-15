# CCT create_user_script

This is used for automatically creating Email accounts on http://kas.all-inkl.com

## Requirements
- Selenium 3.4.1
- geckodriver 0.16.0
- Firefox

To install selenium type `pip install selenium`.

You can get geckodriver [here](https://github.com/mozilla/geckodriver/releases) and add geckodriver to PATH. To do this move the `geckodriver` file to `/usr/local/bin`.

You also need a config.py file which includes the allinkl_username, allinkl_pw and the email_pw of info@service-cct.de. You can just rename `config.sample.py` and fill in the fields.
`cp config.sample.py config.py`.

You also need a csv file named interessenten.csv. You can again just rename to `interessenten.sample.csv` with `cp interessenten.sample.csv interessenten.csv`.
The format should be `first_name,last_name,email_address`. One row per user you want to create.

## Output
A `output.txt` file with all the resulting emails for easy copy-pasting into KAS. Just copy and paste it into the right mailing lists.
