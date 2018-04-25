# NYC Parking Ticket Checker

I was interested in writing something to be able to see what tickets I
have outstanding programmatically and saw that
[drassi/nyc-parking-ticket-monitor](https://github.com/drassi/nyc-parking-ticket-monitor)
existed. Unfortunately the end-point used there
(`http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain`) is now behind a
reCAPTCHA challenge making it infeasible to use.

Instead I used the payments end-point
(`http://www1.nyc.gov/assets/finance/jump/pay_parking_camera_violations.html`)
to perform a similar query.

## Libraries

Requires `mechanize` and `BeautifulSoup4` to be installed.

## Installing

`python setup.py install`

Run `ticket_checker`

### Dev dependencies

`pip install twine`

`pip install wheel`

## Usage

```
usage: ticket_checker.py [-h] [--violation VIOLATION] [--plate PLATE]
                         [--state STATE] [--plate_type PLATE_TYPE] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --violation VIOLATION
                        Violation #
  --plate PLATE         License Plate #
  --state STATE         2-letter State of the license plate, defaults to "NY"
  --plate_type PLATE_TYPE
                        3-character type of the license plate, defaults to
                        "PAS" (passenger)
  --debug               Turns on debugging of HTTP calls.
```

## Examples

Check for a specfic violation number:

`python ticket_checker.py --violation VIOLATION_NUMBER`

Check for your NY plate:

`python ticket_checker.py --plate COOLPL8`

Check for your Montana plate:

`python ticket_checker.py --plate COOLPL8 --state MT`

Check for your NY commerical plate:

`python ticket_checker.py --plate T0000000 --type COM`

## Example output

If a ticket is found the output will look like:

```
$ python ticket_checker.py --plate COOLPL8
Found 1 ticket(s) for COOLPL8
Got tickets:
  1. NO PARKING-STREET CLEANING: violation # 1234567890 for plate COOLPL8 NY PAS on 01/23/2017 for $45.00
```

If there is an error, the script will print the error message returned from the server:

```
$ python ticket_checker.py --plate BADPLATE
"The host system returned the following failure:The plate number was not found. Please verify the plate number, state and type values and search again. Please note if your ticket was recently issued or if you have no outstanding violations, your plate information will not be found. If you wish to pay a ticket you just received, search by the ticket number to ensure it has not been entered into the system. (Error code: PWS-00001) "
```

## Future Plans

 - Add support for multiple violations and plates.

## Packaging

`python setup.py sdist`

`python setup.py bdist_wheel`

### Test PyPI

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

### Prod PyPI

twine upload dist/*

## License

[Apache 2.0](https://opensource.org/licenses/Apache-2.0)
