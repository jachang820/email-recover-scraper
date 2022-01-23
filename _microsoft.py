config = {
  'num_fields': 1,

  'entry': r'https://login.live.com/',
  
  'entry_input': "//input[@type='email']",
  
  'entry_button': "//input[@value='Next']",

  'entry_unload': "//input[@value='Next']",
  
  'pages': [{ # Forgot password?
    'load': "//a[text()='Forgot password?']",
    'next': "//a[text()='Forgot password?']",
    'unload': "//a[text()='Forgot password?']"

  }, { # Show more verification methods
    'load': "//a[text()='Show more verification methods']",
    'next': "//a[text()='Show more verification methods']",
    'unload': "//a[text()='Show more verification methods']"

  }, { # Phone
    'load': "//span[contains(text(), '***')]",
    'matches': {
      'name': 'phone',
      'xpath': "//span[contains(text(), '***')]",
      'function': lambda x: x.text.split(' ')[-1] },
    'next': "//input[@value='Cancel']",
    'unload': '''//a[text()="I don't have any of these"]'''

  }, { # Default screen
    'load': "//div[contains(text(), 'get your security code')]",
    'next': "//input[@value='Cancel']",
    'unload': '''//a[text()="I don't have any of these"]'''

  }],

  'exit_xpath': (
    '''//div[@class="row secondary-text form-group"][2]/'''\
    '''a[text()="I don't have any of these"]'''),
  'max_pages_seen': 3
}