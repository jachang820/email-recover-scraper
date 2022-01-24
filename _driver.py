import time
import random
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, \
  StaleElementReferenceException

driver = None
output = {}
config = None
page = None
loading_time = ()
pages_seen = 0

def set_driver(driver_to_set):
  global driver
  driver = driver_to_set


def configure(config_):
  global config
  config = config_
  random.seed()


def set_loading_time_range(min_sec=1, max_sec=2.5):
  global loading_time
  loading_time = (min_sec, max_sec)


def loading_wait_time():
  return random.uniform(*loading_time)


def find(xpath):
  try:
    element = driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
    element = False
  return element


def enter_email(email):
  global current_next_button
  driver.get(config['entry'])

  find(config['entry_input']).send_keys(email)
  next_button = find(config['entry_button'])
  click_next(next_button)
  unload_page(find(config['entry_unload']))


def check_load_elements(timeout):
  element = False
  current_page = None
  start_time = time.time()

  while not element:
    for page in config['pages']:
      load_xpaths = page['load']
      if not isinstance(load_xpaths, list):
        load_xpaths = [load_xpaths]

      for xpath in load_xpaths:
        element = find(xpath) or element

      if element:
        current_page = page
        break
    if current_page is not None or time.time() - start_time > timeout:
      break
  return current_page


def page_is_loaded(timeout=10): # quit after (timeout) seconds
  global page, pages_seen
  time.sleep(loading_wait_time())
  page = check_load_elements(timeout=10)

  if page:
    pages_seen += 1

  return page


def add_to_output(name, value):
  output[name] = value


def check_matches():
  if 'matches' in page:
    matches = page['matches']
    if not isinstance(matches, list):
      matches = [matches]

    for match in matches:
      if match['name'] not in output:
        element = find(match['xpath'])
        if element:
          result = match['function'](element)
          if result:
            add_to_output(match['name'], result)


def unload_page(indicator_element):
  while True:
    try:
      text = indicator_element.text
    except (StaleElementReferenceException, AttributeError):
      break


def click_next(button_element):
  try:
    button_element.click()
  except:
    try:
      driver.execute_script("arguments[0].click()", button_element)
    except:
      raise ValueError("Button element not clickable")



def next_step():
  click_next(find(page['next']))
  unload_page(find(page['unload']))


def exit_condition():
  if len(output) >= config['num_fields']:
    return True

  xpaths = config['exit_xpath']
  if not isinstance(xpaths, list):
    xpaths = [xpaths]

  element_exists = False
  for xpath in xpaths:
    element_exists = find(xpath)
    if element_exists:
      break

  too_many_pages = (pages_seen >= config['max_pages_seen'])

  return element_exists or too_many_pages