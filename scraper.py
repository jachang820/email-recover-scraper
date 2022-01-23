#!/usr/bin/python3

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
  TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import importlib
import _args
from _driver import *


DEFAULT_EMAIL = 'some_email@domain.com'


if __name__ == '__main__':
  # Enter email on command line as in ./scraper.py email
  email, service, parser = _args.handle_args()
  config = importlib.import_module('_' + service).config
  parser.print_help() # Delete this line if you don't need help

  if email is None: # or manually
    email = DEFAULT_EMAIL

  options = uc.ChromeOptions()
  options.add_argument("--incognito")
  driver = uc.Chrome(options=options)

  set_driver(driver)
  configure(config)
  loading_wait_time(1) # seconds to wait for page to load

  # Enter email address and click next
  enter_email(email)

  while True:

    # Wait for element to load before continuing
    load_element = page_is_loaded(timeout=15) # quit after some seconds
    if not load_element:
      print("Timeout")
      driver.quit()
      break

    check_matches()

    # Click button for next screen
    if exit_condition():
      break
    
    else:
      next_step()
