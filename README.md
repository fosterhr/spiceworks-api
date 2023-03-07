# Spiceworks API

This is a web scraper built with Flask and Selenium that extracts data from Spiceworks. The script uses a pool of Selenium drivers to increase the speed of the scraping process.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `Flask` and `Selenium`.

```bash
pip install Flask selenium
```

## Configuration

Before running the script, you need to set the following constants:
- `BASE_UR`: the base URL of the target website
- `USER_EMAIL`: the email address of the user account to use for authentication
- `USER_PASSWORD`: the password of the user account to use for authentication
- `DRIVER_POOL_SIZE`: the number of Selenium drivers to use for the scraping process

You can set these constants in the script file itself.


## Usage

To run the script, simply execute the following command:
```
python app.py
```

This will start the Flask application on port 80. You can access the API endpoints by visiting the following URLs:
- `/api/tickets/`: returns all tickets
- `/api/tickets/<status>`: returns tickets with a specific status
- `/api/users`: returns all users

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

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
