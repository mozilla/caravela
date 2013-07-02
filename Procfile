web: /srv/caravela/bin/gunicorn --bind=127.0.0.1:$PORT --error-logfile -  --log-file - web:app

workers:  /srv/caravela/bin/celeryd -A web.tasks -c 3 --loglevel=info --time-limit=60
clock:  /srv/caravela/bin/celerybeat -A web.tasks
