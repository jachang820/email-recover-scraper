# Use the code in this file to execute the scraper from another script

import sys

email_address = 'f'
service = 'apple'

old_argv = sys.argv
sys.argv = ['./scraper.py', '--email', email_address, '--service', service]
with open('./scraper.py', 'r') as file:
  bytecode = compile(file.read(), 'scraper', 'exec')
  exec(bytecode)

sys.argv = old_argv


# This works too!
# ---------------------------------------------------------------
# import subprocess

# email_address = 'f'
# service = 'apple'

# subprocess.run('python ./scraper.py --email {0} --service {1}'.format(
#   email_address, service))