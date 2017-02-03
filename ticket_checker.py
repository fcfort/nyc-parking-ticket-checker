import argparse
import logging
import mechanize
import re
import sys
from bs4 import BeautifulSoup

def get_violations(soup):
  violation_list = []
  violations = soup.find_all(
      class_='violation-group-detail-wrapper expander-content')
  for violation_tag in violations:
    violation_values = violation_tag.find_all(
      class_='violation-details-single-value1')
    violation = {}
    violation['number'] = violation_values[0].string
    violation['plate'] = violation_values[1].string
    violation['description'] = violation_values[2].string
    violation['issue_date'] = violation_values[3].string
    violation['amount'] = violation_values[4].string
    # image_url_on_click = violation_tag.find(class_='nav-link').a['onclick']
    violation_list.append(violation)
  return violation_list

BEAUTIFUL_SOUP_PARSER = 'html.parser'

parser = argparse.ArgumentParser()
parser.add_argument('--violation', help='Violation #')
parser.add_argument('--plate', help='License Plate #')
parser.add_argument(
  '--state', help='2-letter State of the license plate, defaults to "NY"')
parser.add_argument(
  '--plate_type',
  help='3-character type of the license plate, defaults to "PAS" (passenger)')
parser.add_argument(
  '--debug', action='store_true', help='Turns on debugging of HTTP calls.')
args = parser.parse_args()

if args.violation and args.plate or not args.violation and not args.plate:
  print 'Specify either a violation # or license plate #.'
  sys.exit(1)

br = mechanize.Browser()

# Log debug information about HTTP redirects and Refreshes.
if args.debug:
  logger = logging.getLogger("mechanize")
  logger.addHandler(logging.StreamHandler(sys.stdout))
  logger.setLevel(logging.DEBUG)
  br.set_debug_http(True)
  br.set_debug_responses(True)
  br.set_debug_redirects(True)

# Get first URL
br.open(
  'http://www1.nyc.gov/assets/finance/jump/'
  'pay_parking_camera_violations.html')

# Follow redirect contained in iframe src
soup = BeautifulSoup(br.response().read(), BEAUTIFUL_SOUP_PARSER)
br.open(soup.body.iframe['src'])

# Set violation #

br.select_form(nr=0) # Form has no `name`

# Because there is both a non-mobile and mobile version on the page, we need
# to find the first one and set it.
if args.violation:
  br.find_control(name='args.VIOLATION_NUMBER_NOL', nr=0).value = args.violation
  query = [args.violation]
elif args.plate:
  br.find_control(name='args.PLATE', nr=0).value = args.plate
  query = [args.plate]
  if args.state:
    br.find_control(name='args.STATE', nr=0).value = [args.state,]
    query.append(args.state)
  if args.plate_type:
    br.find_control(name='args.TYPE', nr=0).value = [args.plate_type,]
    query.append(args.plate_type)

query_string = ", ".join(query)

# Remove duplicate form controls, otherwise we get an error from the server.
form_names_set = set([])
for control in br.form.controls[:]:
  if control.name in form_names_set:
    br.form.controls.remove(control)
  else:
    form_names_set.add(control.name)

# Submit form
br.submit()

# Look for violation response text

html = br.response().read()
soup = BeautifulSoup(br.response().read(), BEAUTIFUL_SOUP_PARSER)

# Errors are put into a class `global-violation-prompt` div tag.
error_tags = soup.find_all(class_='global-violation-prompt')

if error_tags:
  for tag in error_tags:
    print tag.string
else:
  match = re.search(r'No matches found for your violation search', html)
  if match:
      print 'No tickets found for ' + query_string
  else:
    # Parse list of violations found:
      print 'Found tickets for ' + query_string
      print 'Got tickets: ' + '\n'.join([str(violation) for violation in get_violations(soup)])
