import sys
import argparse

def handle_args():
  parser = argparse.ArgumentParser(prog="scraper",
  description='Retrieve user information from email recovery.')
  parser.add_argument('--email', 
    help='email address to look up')
  parser.add_argument('--service', default='gmail',
    choices=['gmail', 'apple', 'microsoft'], 
    help='email service to query')

  args = parser.parse_args()
  email = args.email.encode('ascii', 'ignore').decode()
  service = args.service.encode('ascii', 'ignore').decode()
  return email, service, parser