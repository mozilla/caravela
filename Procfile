web: /srv/caravela/bin/gunicorn --bind=127.0.0.1:$PORT --error-logfile -  --log-file - web:app

workers:  /srv/caravela/bin/celeryd -A web.tasks -c 3 --loglevel=info --time-limit=60
clock:  /srv/caravela/bin/celerybeat -A web.tasks

# testing and maintnance commands
db: /srv/caravela/bin/python -i db.py /tmp/data/reduce\:0-64-950
tests: /srv/caravela/bin/nosetests -s 
solo-worker:  /srv/caravela/bin/celeryd -A web.tasks --pool=solo
solo-web:  /srv/caravela/bin/python run.py