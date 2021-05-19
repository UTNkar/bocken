# bocken
A digital journal system for UTN's car Bocken

# Installing
1. Install Python 3, at least version 3.8 or up.
2. [Install NodeJs](https://nodejs.org) and npm (npm is included in the nodejs installation). This is needed for tailwind.
3. [Install postgresql](INSTALLING_POSTGRES.md)
4. Install the following packages (with apt on ubuntu):
   - python3-venv
   - python3-dev
   - build-essentials
   - libpq-dev
5. Clone the repository.
6. Copy the file `.env-template` and name the copy `.env`
7. Fill in the following variables in `.env`. Uncomment only the variables that you fill in a value:
    1. `DJANGO_DB_NAME`: The name of the database you created in step 2. (default value: bocken)
    2. `DJANGO_DB_USER`: The name of the database user you created in step 2. (default value: bocken)
    3. `DJANGO_DB_PASS`: The password for the database user you created in step 2. (no default value)
    4. `DJANGO_DB_HOST` (default value: localhost) and `DJANGO_DB_PORT` (default value: 5432): **You only have to fill in these if you have setup your database to not be hosted on the default host and port**. If you followed the steps in step 2, you should not have to set these.
    5. (optional) `DJANGO_SECRET`: The secret key that django uses. You can fill in this to a custom value but you don't have to.
9. Run `source ./source_me.sh` to create a virtual environment.
10. Run `pip install --upgrade pip` to make sure that pip is running the latest version
11. Run `pip install -r dev-requirements.txt`
12. Use `cd src` to enter the website directory.
13. Run `./manage.py tailwind init` to install tailwind
13. Run `./manage.py migrate` to initialize the database.
14. Run `./manage.py compilemessages` to create all translations
15. Run `./manage.py createsuperuser` to create an admin user that you will use to log in to the admin pages.

The journal system is now installed!

During development, you need to use two terminals. **Dont forget to run `source ./source_me.sh` in both terminals before running these commands!**

1. In one run the command `./manage.py runserver` to start the django server.
2. In the other run `./manage.py tailwind start` to start tailwind.

You can now visit the journal system on `http://localhost:8000`.

## Documentation

Documentation for the journal system can be found on [docs.utn.se](https://docs.utn.se/)

## Testing

All code in this repository is tested in two ways: we use [Django test
suites](https://docs.djangoproject.com/en/3.1/topics/testing/) and we run the
[flake8](http://flake8.pycqa.org/en/latest/) style enforcer. Together they can
promote clean and good code.

These tests are run automatically using Github Actions.
If, however, you want to run these tests locally you can run the following
commands in the project root directory:

- `./src/manage.py test src` - to test with our Django test suites
- `flake8 src` - to run the flake8 style enforcer

## Translating

Project Moore intends to be multilingual. The web application is available in
both Swedish and English. Whenever any translatable text is added or changed it
should be translated using translation files.

To create or edit translations:

1. `cd src/`
1. `./manage.py makemessages -l sv`
2. This will create or update the files under `src/bocken/locale/`.
3. Edit the translations in your editor
4. Run `./manage.py compilemessages` for the changes to take effect

## Tailwind
The journal system uses a css framework for the frontend called [Tailwind](https://tailwindcss.com/) and it is installed via the pip package [django-tailwind](https://pypi.org/project/django-tailwind/). Tailwind adds a bunch of css classes that do only one thing. For example the class `bg-red-400` adds a red background, the 400 is one of the predefined red colors that tailwind offers. The idea of tailwind is that instead of creating a bunch of css classes with many attributes, you add these classes on the HTML elements directly and thus not having to write any own css.

It should be noted that it is not used in the admin pages since those pages uses their own predefined styling
