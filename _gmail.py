_span = lambda text: '''//span[text()="{0}"]'''.format(text)
_span_button = lambda text: '{0}/parent::button'.format(_span(text))


def _get_devices(div):
  # Get first sentence
  sentence = div.text.split('.')[0]

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
  
  'entry_button': "//div[@id='identifierNext']//button",

  'entry_unload': "h1[@id='headingText']/span('Sign in')",
  
  'pages': [{ # Forgot password?
    'load': [
      "//div[@id='forgotPassword']//button",
      "//div[text()='Enter your password']"],
    'next': "//div[@id='forgotPassword']//button",
    'unload': "//div[@id='forgotPassword']//button"

  }, { # Do you have your phone?
    'load': "//strong[text()='Do you have your phone?']",
    'next': _span_button("Try another way"),
    'unload': "//strong[text()='Do you have your phone?']"

  }, { # Google prompts disabled
    'load': "//div[contains(text(), 'Google prompts are disabled')]",
    'next': _span_button("More ways to sign in"),
    'unload': _span_button("More ways to sign in")

  }, { # Last password
    'load': "//div[starts-with(text(), 'Enter the last password')]",
    'next': _span_button("Try another way"),
    'unload': _span_button("Try another way")

  }, { # Device
    'load': "//span[starts-with(text(), 'Check your')]",
    'matches': {
      'name': 'device',
      'xpath': "//div[contains(text(), 'sent a notification')]",
      'function': _get_devices },
    'next': _span_button("Try another way"),
    'unload': _span_button("Try another way")

  }, {
    'load': "//li[contains(text(), 'Get your')]",
    'matches': {
      'name': 'device',
      'xpath': "//li[contains(text(), 'Get your')]",
      'function': lambda x: ' '.join(x.text.split(' ')[2:]) },
    'next': _span_button("Try another way"),
    'unload': _span_button("Try another way")

  }, { # Use the Camera app on your iPhone to scan this QR code
    'load': "//span[contains(text(), 'QR code')]",
    'matches': {
      'name': 'device',
      'xpath': "//li[contains(text(), 'QR code')]",
      'function': lambda x: ' '.join(x.text.split(' ')[6]) },
    'next': _span_button("Try another way"),
    'unload': _span_button("Try another way")

  }, { # Trusted email
    'load': [
      "//div[contains(text(), 'recovery email address')]",
      "//div[contains(text(), 'email with a verification code')]"],
    'matches': {
      'name': 'email',
      'xpath': "//span[contains(text(), '•')]",
      'function': lambda x: x.text.strip() },
    'next': _span_button("Try another way"),
    'unload': "//div[@id='idvpreregisteredemailNext']//button"

  }, { # Phone, email
    'load': [
      "//div[contains(text(), 'Confirm the phone number')]",
      "//div[contains(text(), 'send a verification code')]"],
    'matches': [{
      'name': 'email',
      'xpath': "//span[contains(text(), '@')]",
      'function': lambda x: x.text.strip() 
    }, {
      'name': 'phone',
      'xpath': "//span[contains(text(), '•')]",
      'function': lambda x: x.text.strip() }],
    'next': [
      _span_button("I don’t have my phone"),
      _span_button("Try another way")],
    'unload': "//div[@id='smsButton']//button"
    
  }, {
    'load': _span("Choose how you want to sign in:"),
    'matches': [{
      'name': 'email',
      'xpath': "//span[contains(text(), '@')]",
      'function': lambda x: x.text.strip()
    }, {
      'name': 'phone',
      'xpath': "//span[contains(text(), '•')]",
      'function': lambda x: x.text.strip(),
      'multiple': True }],
    'next': "//div[text()='Try another way to sign in']",
    'unload': "//div[text()='Try another way to sign in']"

  }, { # Failed screen
    'load': [
      "//div[contains(text(), 'Google needs to confirm this account')]",
      "//div[contains(text(), 'Google couldn’t verify')]"],
    'next': "//div[@id='profileIdentifier']",
    'unload': "//div[@id='profileIdentifier']"

  }],

  'exit_xpath': [
    "//div[contains(text(), 'Google needs to confirm this account')]",
    "//div[contains(text(), 'Google couldn’t verify')]",
    _span_button("Try again")],
  'max_pages_seen': 6
}
