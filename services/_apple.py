config = {
  'num_fields': 1,

  'entry': r'https://iforgot.apple.com/password/verify/appleid',
  
  'entry_input': "//div[@class='form-textbox ']/input",
  
  'entry_button': "//div[text()='Continue']",

  'entry_unload': "//h1[text()='Having trouble signing in?']",
  
  'pages': [{ # Trusted email
    'load': "//div[contains(text(), 'email address ending in')]",
    'matches': {
      'name': 'email',
      'xpath': "//label[contains(text(), '•')]",
      'function': lambda x: x.text.strip() },
    'next': "//button[@id='cancel']",
    'unload': "//button[@id='cancel']"

  }, { # Phone
    'load': "//p[contains(text(), 'phone number')]",
    'matches': {
      'name': 'phone',
      'xpath': "//li[contains(text(), '•')]",
      'function': lambda x: x.text.strip() },
    'next': "//div[text()='Cancel']",
    'unload': "//div[text()='Cancel']"
  }],

  'exit_xpath': [
    "//button[@id='cancel']",
    "//div[text()='Cancel']"],
  'max_pages_seen': 1
}