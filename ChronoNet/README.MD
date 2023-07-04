# ChronoNet

## Directory Navigation
- [Settings](./config/settings/)
  - [Base](./config/settings/base.py)
  - [Development](./config/settings/development.py)
  - [Production](./config/settings/production.py)
- [Accounts](./account/)
- [Templates](./templates/)
  - [Home](./templates/home.html)
  - [Main](./templates/main.html)
  - [Header/Footer](./templates/layout/)
- [Posts](./post/)
- [Static (CSS, etc.)](./static/)

---
## Getting Set-Up

You need to have an environment file __before__ you can actually run the project.

There is currently a [.env](.env) file in this directory which works if you don't want to make your own.

**NOTE:** Make sure to change the `DJANGO_SETTINGS_MODULE` to **development** if running on localhost.


- Look at the '.env.example' file if you want to make your own
  - this will be a basic template for some environment variables
- Make sure `python-dotenv` is installed on your machine if running locally
  - use `python -m pip install python-dotenv` if you don't have it installed
- Generate a secret key (there is no longer a pre-generated one in the settings)
  - you can use `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())`
  - put that secret key in your .env file (it will be accessed in the settings)
- Consider changing the secret admin url for your machine


---

## Running the Server

Once you have a `.env` file, you can run the server by completing the following steps:

- Install the required modules
  - `python -m pip install -r requirements.txt`
- You may need to perform some migrations
  - `python manage.py makemigrations; python manage.py migrate`
- Run the server
  - `python manage.py runserver`
  - this will start the server on your local system
  - navigate to the URL given to access the website

There is also a [Makefile](Makefile) that can do all of this for you
  - **NOTE:** make does not always work well (or at all) with Windows 
  - run `make help` to see options