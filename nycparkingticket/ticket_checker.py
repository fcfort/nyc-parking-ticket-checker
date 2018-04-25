import argparse
import collections
import datetime
import logging
import re
import sys

import mechanize
from bs4 import BeautifulSoup


BEAUTIFUL_SOUP_PARSER = 'html.parser'

VIOLATIONS_URL = ('http://www1.nyc.gov/assets/finance/jump/'
    'pay_parking_camera_violations.html')

DELETED_VIOLATION_PATTERN = 'Violation Entered has been flagged as deleted'
INVALID_VIOLATION_NUMBER_PATTERN = 'Invalid Violation Number'
NO_RESULTS_FOR_PLATE = 'The plate number was not found.'


Violation = collections.namedtuple(
    'Violation', 'description number plate issue_date amount')


class TicketCheckerQueryException(Exception):
  pass


class InvalidViolationNumberException(TicketCheckerQueryException):
  pass


class _Query(object):
  def __init__(self,
      state=None, plate_type=None, plate_number=None, violation_number=None):
    self.state = state
    self.plate_type = plate_type
    self.plate_number = plate_number
    self.violation_number = violation_number

  @classmethod
  def byViolationNumber(cls, violation_number):
    return cls(violation_number=violation_number)

  @classmethod
  def byPlate(cls, state, plate_type, plate_number):
    return cls(state=state, plate_type=plate_type, plate_number=plate_number)


class TicketChecker(object):

  def __init__(self, debug=False):
    self._br = mechanize.Browser()

    if debug:
      # Log debug information about HTTP redirects and Refreshes.
      logger = logging.getLogger("mechanize")
      logger.addHandler(logging.StreamHandler(sys.stdout))
      logger.setLevel(logging.DEBUG)
      self._br.set_debug_http(True)
      self._br.set_debug_responses(True)
      self._br.set_debug_redirects(True)

  def getByViolationNumber(self, violation_number):
    return self._parseViolations(_Query.byViolationNumber(violation_number))

  def getByPlate(self, plate_number, state=None, plate_type=None):
    return self._parseViolations(
        _Query.byPlate(state, plate_type, plate_number))

  def _parseViolations(self, query):
    # Get first URL
    self._br.open(VIOLATIONS_URL)

    # Follow redirect contained in iframe src
    soup = BeautifulSoup(self._br.response().read(), BEAUTIFUL_SOUP_PARSER)
    self._br.open(soup.body.iframe['src'])

    # Set query parameters to form

    self._br.select_form(nr=0) # Form has no `name`

    # Because there is both a non-mobile and mobile version on the page, we need
    # to find the first one and set it.
    if query.violation_number:
      self._br.find_control(
          name='args.VIOLATION_NUMBER_NOL', nr=0).value = query.violation_number
    elif query.plate_number:
      self._br.find_control(name='args.PLATE', nr=0).value = query.plate_number
      if query.state:
        self._br.find_control(name='args.STATE', nr=0).value = [query.state,]
      if query.plate_type:
        self._br.find_control(
            name='args.TYPE', nr=0).value = [query.plate_type,]

    # Remove duplicate form controls, otherwise we get an error from the server.
    form_names_set = set([])
    for control in self._br.form.controls[:]:
      if control.name in form_names_set:
        self._br.form.controls.remove(control)
      else:
        form_names_set.add(control.name)

    # Submit form
    self._br.submit()

    # Look for violation response text

    html = self._br.response().read()
    soup = BeautifulSoup(self._br.response().read(), BEAUTIFUL_SOUP_PARSER)

    # Errors are put into a class `global-violation-prompt` div tag.
    error_tags = soup.find_all(class_='global-violation-prompt')

    # Common cases when violation paid or non-existent

    if DELETED_VIOLATION_PATTERN in html:
      return []
    elif NO_RESULTS_FOR_PLATE in html:
      return []
    elif INVALID_VIOLATION_NUMBER_PATTERN in html:
      raise InvalidViolationNumberException()

    if error_tags:
      raise TicketCheckerQueryException(str([tag.string for tag in error_tags]))
    else:
      match = re.search(r'No matches found for your violation search', html)
      if match:
        return []  # No tickets found
      else:
        # Parse list of violations found:
        return TicketChecker.get_violations(soup)

  @staticmethod
  def get_violations(soup):
    violation_list = []
    violations = soup.find_all(class_='violation-group-detail')

    for violation_tag in violations:
      violation_values = violation_tag.find_all(
        class_='violation-details-single-value1')
      violation = Violation(
          number=violation_values[0].string,
          plate=violation_values[1].string,
          description=violation_values[2].string,
          issue_date=datetime.datetime.strptime(
              violation_values[3].string, '%m/%d/%Y').date(),
          # image_url_on_click = violation_tag.find(class_='nav-link').a['onclick']
          amount=violation_values[4].string)

      violation_list.append(violation)
    return violation_list


def main():
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

  ticket_checker = TicketChecker(debug=args.debug)

  if(args.violation):
    violations = ticket_checker.getByViolationNumber(
        violation_number=args.violation)
  else:
    violations = ticket_checker.getByPlate(
        plate_number=args.plate,
        plate_type=args.plate_type,
        state=args.state)

  if not violations:
      print 'No tickets found for ' + str(args)
  else:
    print ('Found {} ticket(s) for ' + str(args)).format(len(violations))
    print 'Got tickets:'
    for i, violation in enumerate(violations):
      print '\t{}. {}: violation # {} for plate {} on {} for ${}'.format(
          i + 1,
          violation.description,
          violation.number,
          violation.plate,
          violation.issue_date,
          violation.amount)
