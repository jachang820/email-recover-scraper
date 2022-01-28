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
  email, service, quiet_mode, parser = _args.handle_args()
  config = importlib.import_module('services._' + service).config

  if not quiet_mode:
    parser.print_help() # Delete this line if you don't need help

  if email is None: # or manually
    email = DEFAULT_EMAIL

  options = uc.ChromeOptions()
  options.add_argument("--incognito")
  driver = uc.Chrome(options=options)

  set_driver(driver)
  configure(config)
  set_loading_time_range(1., 2.5) # seconds to wait for page to load

  # Enter email address and click next
  enter_email(email)

  past_matches = set()

  while True:

    # Wait for element to load before continuing
    load_element = page_is_loaded(timeout=15) # quit after some seconds
    if not load_element:
      print("Timeout")
      driver.quit()
      break

    check_matches()
    if not quiet_mode:
      for key, values in output.items():
        for value in values:
          if value not in past_matches:
            print("{0}: {1}".format(key, value))
            past_matches.add(value)

    # Click button for next screen
    if exit_condition():
      break
    
    else:
      next_step()
