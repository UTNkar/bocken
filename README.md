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
7. Fill in the necessary variables in `.env`. All variables have defaults which can be found in `bocken/settings/dev.py`. If you need to override these defaults, uncomment the variable in `.env` and set its value.
8. Run `source ./source_me.sh` to create a virtual environment.
9. Run `pip install --upgrade pip` to make sure that pip is running the latest version
10. Run `pip install -r dev-requirements.txt`
11. Use `cd src` to enter the website directory.
12. Run `./manage.py migrate` to initialize the database.
13. Run `./manage.py compilemessages` to create all tranlsations
14. Run `./manage.py createsuperuser` to create an admin user.

During development, you can run a test web server using `./manage.py runserver`.

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
