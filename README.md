# BDO Chronicle

BDO Chronicle is a utility web site for the game
[Black Desert Online](https://www.blackdesertonline.com/). It currently deals
with **Nodes** and **Crafting**, although future endeavors can't be ruled out.

![Build Status](https://travis-ci.org/zsommers/bdo_chronicle.svg?branch=master)
![Coverage Status](https://coveralls.io/repos/github/zsommers/bdo_chronicle/badge.svg?branch=master)

## Development
This is currently being developed by one person, so while
[Issues](https://github.com/zsommers/bdo_chronicle/issues) requesting features
are welcome it may take a while. If you are interested in contributing, feel
free to fork this repo and make pull requests.

### Setup
This is [Python](https://www.python.org/) project targeting Python3. As such,
you will need that installed. I also recommend
[virtualenv](https://virtualenv.pypa.io/en/latest/) and
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) and
will provide instructions for those. I've heard good things about
[pyvenv](https://docs.python.org/3/library/venv.html) but can't help with it.

Additionally, you'll probably want a local
[PostgreSQL](http://www.postgresql.org/) server. For OSX I recommend
[Postgres.app](http://postgresapp.com/).

#### Create the environment and clone your fork
You'll need to run command similar to these.

```bash
mkproject -p `which python3` bdo_chronicle

# This should move you to the new project directory

git clone git@github.com:<your_github_name>/bdo_chronicle.git

pip install -r requirements/dev.txt
```

This should get the project and its dependencies set up. However, you'll want
to add some environment variables to the project's `postactivate` script.

```bash
# The script is typically located here:
#   ~/.virtualenvs/bdo_chronicle/bin/postactivate

export DJANGO_SETTINGS_MODULE=bdo_tools.settings.dev
export PYTHONPATH=$PYTHONPATH:<path to your projects dir>/bdo_chronicle/bdo_tools

export DJANGO_SECRET_KEY=supersecret

export BDO_DB_USER=<local postgres username>
export BDO_DB_PASSWORD=<if you have a local postgres password>
export BDO_DB_HOST=localhost
export BDO_DB_PORT=5432
export BDO_DB_NAME=bdo
```

After saving `postactivate`, you'll need to `deactivate` and
`workon bdo_chronicle`. After re-initializing the virtualenv, you should be
able to use the `django-admin` command.

#### Running the server
I have this project running on [Heroku](https://www.heroku.com) at
[bdo.zachsommers.com](http://bdo.zachsommers.com/admin/). Please
[email me](bdo@zachsommers.com) if you'd like an account to check the project
out. If you want to run your own instance, please feel free!

For development or personal use, running
[Django](https://www.djangoproject.com/)'s development server is quite simple:

```bash
django-admin runserver
```

#### Running tests
Any contributed code is expected to also have tests. Ideally a pull request
will not reduce the project's code coverage.

Running tests is a breeze:

```bash
py.test

# Get details, including test names
py.test -v
```

If you'd like to preview your test coverage before pushing to
[GitHub](https://github.com), you'll need some additional installs.

```bash
# You can use the CI requirements ...
pip install -r requirements/ci.txt

# ... or you can manually install the library
pip install pytest-cov

# Tests can now be run with coverage:
py.test --cov=bdo_tools
```

## Project Layout
This is a basic overview of some of the structure that may not be immediately
apparent.

#### Requirements and settings
You can see in both `requirement/` and `bdo_tools/bdo_tools/settings/` there
are a number of files. In addition to `base` there are `dev`, `ci`, and `prod`.
This allows all common requirements or settings to live in the repective base
file while requirements or settings that only apply part of the time live in
the specialized files. All of the specialized files import `base`.
