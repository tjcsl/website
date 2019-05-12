# tjCSL: Website: Setup

## Set-Up a Development Environment

* Ensure you have [Python](https://python.org) and [Git](https://git-scm.com/) installed with some sort of terminal.
* Clone the repository to your local computer with `git clone git@github.com:tjcsl/website` (if you have GitHub SSH keys setup) or `git clone https://github.com/tjcsl/website`
* `cd` into the directory
* Head over to https://ion.tjhsst.edu/oauth/register to register an Ion OAuth application.
    * Fill in a name for your application
    * Select `Confidential` for `Client Type`
    * Select `Authorization Code` for `Authorization Grant Type`
* Copy `tjhsst/settings/secret.sample` to `tjhsst/setttings/secret.py`
* Using your favorite text or code editor, edit `tjhsst/settings/secret.py` to use the client ID and client secret from Ion
* Run `python manage.py migrate` to apply migrations
* Run `python manage.py runserver` to run the development server
* In your web browser, navigate to the directed URL to visit your creation.

## User Accounts
* To login, navigate to http://localhost:8000/login/ion
* To make yourself a superuser, run this in the Django shell (`python manage.py shell`) in another terminal
```
username="<TJ USERNAME>"; from tjhsst.apps.users.models import User; u = User.objects.get(username=username); u.is_superuser = True; u.is_staff = True; u.save()
```
