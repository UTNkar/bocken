# Bocken
A digital journal system for UTN's car Bocken.

# Installing
1. Install Python 3, at least version 3.8 or up.
2. [Install NodeJs](https://nodejs.org) and npm (npm is included in the nodejs installation). This is needed for tailwind.
3. Install the following packages
    - Python virtual environment
        - Ubuntu: `sudo apt install python3-venv`
        - Mac: `brew install virtualenv`
        - Windows: `pip install virtualenv`
    - GNU gettext:
        - Ubuntu: `sudo apt install gettext`
        - Mac: `brew install gettext`
        - Windows: [Download gettext here](https://mlocati.github.io/articles/gettext-iconv-windows.html)
4. Clone the repository.
5. Run `source ./source_me.sh` to create a virtual environment.
6. Run `pip install -r dev-requirements.txt`
7. Use `cd src` to enter the website directory.
8. Run `./manage.py tailwind install` to install tailwind
9. Run `./manage.py migrate` to initialize the database.
10. Run `./manage.py compilemessages` to create all translations
11. Run `./manage.py createsuperuser` to create an admin user that you will use to log in to the admin pages.

The journal system is now installed!

During development, you need to use two terminals. **Dont forget to run `source ./source_me.sh` in both terminals before running these commands!**

1. In one run the command `./manage.py runserver` to start the django server.
2. In the other run `./manage.py tailwind start` to start tailwind.

You can now visit the journal system on `http://localhost:8000`.

### Troubleshooting

#### The styles from tailwind is not loading in the browser

If the styles from tailwind are not loading in the browser, (a.k.a. the css file gets error 404), stop the command that runs the server (`./manage.py runserver`) and then restart it.

This is because django must be restarted when new static files are added which can happen if the django server is started before the tailwind command (which creates the css file for tailwind).

## Documentation

Documentation for the journal system can be found on [docs.utn.se](https://docs.utn.se/bocken_journal_system/)

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

The journal system for Bocken intends to be multilingual. The web application is available in
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

All tailwind documentation and classes can be found on [their website](https://tailwindcss.com/).

It should be noted that it is not used in the admin pages since those pages uses their own predefined styling
