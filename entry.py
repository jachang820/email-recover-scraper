# Use the code in this file to execute the scraper from another script

import sys

email_address = 'katsucats1985'
service = 'gmail'

old_argv = sys.argv
output = None

sys.argv = ['./scraper.py', 
  '--email', email_address, 
  '--service', service, 
  '--quiet']

with open('./scraper.py', 'r') as file:
  bytecode = compile(file.read(), 'scraper', 'exec')
  exec(bytecode)
  output = locals()['output']

sys.argv = old_argv
if len(output) > 0:
  print(output)