# NYC Parking Ticket Checker

I was interested in writing something to be able to see what tickets I have outstanding programmatically and saw that [drassi/nyc-parking-ticket-monitor](https://github.com/drassi/nyc-parking-ticket-monitor) existed. Unfortunately the end-point used there (`http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain`) is now behind a reCAPTCHA challenge making it infeasible to use.

Instead I used the payments end-point (`http://www1.nyc.gov/assets/finance/jump/pay_parking_camera_violations.html`) to perform a similar query.

## Libraries

Requires `BeautifulSoup4` to be installed.

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

## Future Plans

 - Add support for multiple violations and plates.
 - Programmatic output (like JSON or CSV)

## License

[Apache 2.0](https://opensource.org/licenses/Apache-2.0)
