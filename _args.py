import sys
import argparse

def handle_args():
  parser = argparse.ArgumentParser(prog="scraper",
  description='Retrieve user information from email recovery.')
  parser.add_argument('-e', '--email', 
    help='email address to look up')
  parser.add_argument('-s', '--service', default='gmail',
    choices=['gmail', 'apple', 'microsoft'], 
    help='email service to query')
  parser.add_argument('-q', '--quiet', action='store_true',
    help='suppress all output')

  args = parser.parse_args()
  email = args.email.encode('ascii', 'ignore').decode()
  service = args.service.encode('ascii', 'ignore').decode()
  quiet = args.quiet
  return email, service, quiet, parser