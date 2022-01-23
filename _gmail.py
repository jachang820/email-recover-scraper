_span = lambda text: '''//span[text()="{0}"]'''.format(text)


def _get_devices(str):
  # Get first sentence
  sentence = str.split('.')[0]

  # Get everything after 'Google sent a notification to your...'
  device_words = sentence.split(' ')[6:]

  # Get devices as string
  return ' '.join(device_words)


config = {
  'num_fields': 3,

  'entry': r'https://accounts.google.com/signin/v2/identifier?'\
    r'continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&'\
    r'sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
  
  'entry_input': "//input[@type='email']",
  
  'entry_button': _span("Next"),

  'entry_unload': _span("Sign in"),
  
  'pages': [{ # Forgot password?
    'load': [
      _span("Forgot password?"),
      "//div[text()='Try another way to sign in']"],
    'next': _span("Forgot password?"),
    'unload': _span("Forgot password?")

  }, { # Do you have your phone?
    'load': "//strong[text()='Do you have your phone?']",
    'next': _span("Try another way"),
    'unload': "//strong[text()='Do you have your phone?']"

  }, { # Google prompts disabled
    'load': "//div[contains(text(), 'Google prompts are disabled')]",
    'next': _span("More ways to sign in"),
    'unload': _span("More ways to sign in")

  }{ # Last password
    'load': "//div[starts-with(text(), 'Enter the last password')]",
    'next': _span("Try another way"),
    'unload': _span("Try another way")

  }, { # Device
    'load': "//span[starts-with(text(), 'Check your')]",
    'matches': {
      'name': 'device',
      'xpath': "//div[contains(text(), 'sent a notification')]",
      'function': _get_devices },
    'next': _span("Try another way"),
    'unload': _span("Try another way")

  }, {
    'load': "//li[contains(text(), 'Get your')]",
    'matches': {
      'name': 'device',
      'xpath': "//li[contains(text(), 'Get your')]",
      'function': lambda x: ' '.join(x.text.split(' ')[2:]) },
    'next': _span("Try another way"),
    'unload': _span("Try another way")

  }, { # Trusted email
    'load': [
      "//div[contains(text(), 'recovery email address')]",
      "//div[contains(text(), 'email with a verification code')]"],
    'matches': {
      'name': 'email',
      'xpath': "//span[contains(text(), '•')]",
      'function': lambda x: x.text.strip() },
    'next': _span("Try another way"),
    'unload': _span("Try another way")

  }, { # Phone
    'load': [
      "//div[contains(text(), 'Confirm the phone number')]",
      "//div[contains(text(), 'send a verification code')]"],
    'matches': {
      'name': 'phone',
      'xpath': "//span[contains(text(), '•')]",
      'function': lambda x: x.text.strip() },
    'next': _span("I don’t have my phone"),
    'unload': _span("I don’t have my phone")
  }],

  'exit_xpath': _span("Try again"),
  'max_pages_seen': 6
}
