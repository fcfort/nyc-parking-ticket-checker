import argparse
import mechanize
import logging
import re
import sys
from bs4 import BeautifulSoup

BEAUTIFUL_SOUP_PARSER = "html.parser"

logger = logging.getLogger("mechanize")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--violation', help='Violation #')
# parser.add_argument('--plate', help='License Plate #')
# Plate type PAS
args = parser.parse_args()

br = mechanize.Browser()

# Log debug information about HTTP redirects and Refreshes.
# br.set_debug_http(True)
# br.set_debug_responses(True)
# br.set_debug_redirects(True)

# Get first URL
br.open("http://www1.nyc.gov/assets/finance/jump/pay_parking_camera_violations.html")

# Follow redirect contained in iframe src
soup = BeautifulSoup(br.response().read(), BEAUTIFUL_SOUP_PARSER)
iframe_src = soup.body.iframe['src']
br.open(iframe_src)

# Set violation #
br.select_form(nr=0) # Form has no `name`

# Because there is both a non-mobile and mobile version on the page, we need
# to find the first one and set it.
br.find_control(name='args.VIOLATION_NUMBER_NOL', nr=0).value = args.violation

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
# print html
soup = BeautifulSoup(html, BEAUTIFUL_SOUP_PARSER)

# Errors are put into a class `global-violation-prompt` div tag.
error_tags = soup.find_all(class_='global-violation-prompt')

if error_tags:
	for tag in error_tags:
		print tag.string
else:
	match = re.search(r'No matches found for your violation search', html)
	if match:
	    print "No tickets found for violation # " + args.violation
	else:
	    print "Found a ticket for violation # " + args.violation




