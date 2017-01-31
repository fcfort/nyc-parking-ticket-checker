# NYC Parking Ticket Checker

I was interested in writing something to be able to see what tickets I have outstanding programmatically and saw that [drassi/nyc-parking-ticket-monitor](https://github.com/drassi/nyc-parking-ticket-monitor) existed. Unfortunately the end-point used there (`http://nycserv.nyc.gov/NYCServWeb/NYCSERVMain`) is now behind a reCAPTCHA challenge making it infeasible to use.

Instead I used the payments end-point (`http://www1.nyc.gov/assets/finance/jump/pay_parking_camera_violations.html`) to perform a similar query.

## Libraries

Requires `BeautifulSoup4` to be installed.

## Running

`python ticket_checker.py --violation VIOLATION_NUMBER`

Where VIOLATION_NUMBER is the ten-digit violation number found on your ticket.

## Future Plans

 - Add support for plate numbers.
 - Add support for multiple violations and plates.
 - Programmatic output (like JSON or CSV)

## License

[Apache 2.0](https://opensource.org/licenses/Apache-2.0)
