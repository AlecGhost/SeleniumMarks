# SeleniumMarks

## What is it?

SeleniumMarks is a simple script that uses the selenium library to open the webbrowser, go to the THM e-campus website,
download the marks from there and store them as a json file. Furthermore, it is built as a service that sends the
retrieved data to a local server via the [BerrylliumAPI](https://github.com/AlecGhost/BerrylliumAPI), where it can be
accessed by local clients, like
[BerrylliumMobile](https://github.com/AlecGhost/BerrylliumMobile).

## How to use it?

The credentials for the login must be stored in a .env file at the same level or as system wide environment variables. If
they were deposited, hit run, and the script should do its job and store the data as json. The API call can only work if
you have started the local server too and logged in the script as a user. If you don't want to use the API, just comment
out the relevant parts.

## Dependencies

- [selenium](https://github.com/SeleniumHQ/selenium)
- [dotenv](https://github.com/theskumar/python-dotenv)
