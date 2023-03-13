# Spiceworks API

This is a web scraper built with Flask and Selenium that extracts data from Spiceworks. The script uses a pool of Selenium drivers to increase the speed of the scraping process.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `Flask` and `Selenium`.

```bash
pip install -r requirements.txt
```

## Configuration

Before running the script, you need to set the following constants:
- `BASE_URL`: the base URL of the target website
- `USER_EMAIL`: the email address of the user account to use for authentication
- `USER_PASSWORD`: the password of the user account to use for authentication
- `DRIVER_POOL_SIZE` (default 5): the number of Selenium drivers to use for the scraping process

You can set these constants in the script file itself.


## Usage

To run the script, simply execute the following command:
```
python app.py
```

This will start the Flask application on port 80. You can access the API endpoints by visiting the following URLs:
- `/tickets/`: returns all tickets
- `/tickets/id/<id>/`: returns a specific ticket based on it's ID
- `/tickets/user/<user>/`: returns tickets from a specific user
- `/tickets/status/<status>/`: returns tickets with a specific status
- `/users/`: returns all end users
- `/users/<user>`: returns the data for a specific end user
- `/admin/users/`: returns all admin users
- `/admin/users/<user>/`: returns the data for a specific admin user

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## Change Log

- 03/12/2023
  - Added support for ticket and end user/admin user filters.
  - Refactored the drivers into a class-based driver pool.
  - Added `requirements.txt`.
- 03/07/2023
  - Initial commit.

## License

[MIT](https://choosealicense.com/licenses/mit/):
```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
