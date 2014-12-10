# CF example app: ping-pong matching server

This is an app to match ping-pong players with each other. It's currently an
API only, so you have to use `curl` to interact with it.

It has an [acceptance test suite][acceptance-test] you might like to look at.

## Running on [Pivotal Web Services][pws]

Log in.

```bash
cf login -a https://api.run.pivotal.io
```

Target your org / space. An empty space is recommended, to avoid naming collisions.

```bash
cf target -o myorg -s myspace
```

Sign up for a cleardb instance.

```bash
cf create-service cleardb spark mysql
```

Push the app. Its manifest assumes you called your ClearDB instance 'mysql'.

```bash
cf push -n mysubdomain
```

Export the test host

```bash
export HOST=http://mysubdomain.cfapps.io
```

Now follow the [interaction instructions](#interaction-instructions).

NB: By default, the app runs with an insecure, shared
[SECRET_KEY][django-deployment]. If you care about security in your app, you
should set this in an environment variable:

```bash
cf set-env djangopong SECRET_KEY thesecretkeythatonlyyouknow
cf restage djangopong
```

## Running locally

The following assumes you have a working, 3.4.x version of [Python][python]
installed. You'll also need [pip][pip], the Python dependency manager. If you
installed Python using Homebrew on OSX, you're already set. On Ubuntu, the
package you want is 'python3-pip'.

Install and start MySQL:

```bash
brew install mysql
mysql.server start
mysql -u root
```

Create a database user and table in the MySQL REPL you just opened:

```sql
CREATE USER 'djangopong'@'localhost' IDENTIFIED BY 'djangopong';
CREATE DATABASE pong_matcher_django_development;
GRANT ALL ON pong_matcher_django_development.* TO 'djangopong'@'localhost';
exit
```

Install virtualenv:

```bash
pip3 install virtualenv
```

Create and activate a new Python environment:

```bash
virtualenv env
source env/bin/activate
```

Install the project's dependencies:

```bash
pip install -r requirements.txt --allow-external mysql-connector-python
```

Migrate the database:

```bash
./manage.py migrate
```

Start the application server:

```bash
./manage.py runserver
```

Export the test host in another shell, ready to run the interactions.

```bash
export HOST=http://localhost:8000
```

Now follow the [interaction instructions](#interaction-instructions).

NB: you can also use Foreman to run the migrations and start the app server
with `foreman start`. However, foreman defaults to a different port (5000), so
be sure to export the test host with port 5000 instead of 8000.

## Interaction instructions

Start by clearing the database from any previous tests.  You should get a 200.

```bash
curl -v -X DELETE $HOST/all
```

Then request a match, providing both a request ID and player ID. Again, you
should get a 200.

```bash
curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/firstrequest -d '{"player": "andrew"}'
```

Now pretend to be someone else requesting a match:

```bash
curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/secondrequest -d '{"player": "navratilova"}'
```

Let's check on the status of our first match request:

```bash
curl -v -X GET $HOST/match_requests/firstrequest
```

The bottom of the output should show you the match_id. You'll need this in the
next step.

Now pretend that you've got back to your desk and need to enter the result:

```bash
curl -v -H "Content-Type: application/json" -X POST $HOST/results -d '
{
    "match_id":"thematchidyoureceived",
    "winner":"andrew",
    "loser":"navratilova"
}'
```

You should get a 201 Created response.

Future requests with different player IDs should not cause a match with someone
who has already played. The program is not yet useful enough to
allow pairs who've already played to play again.

[acceptance-test]:https://github.com/camelpunch/pong_matcher_acceptance
[pws]:https://run.pivotal.io
[python]:https://www.python.org
[pip]:https://pip.pypa.io/en/latest/
[django-deployment]:https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
