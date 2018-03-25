web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py kennedy.wsgi
worker: bin/start-pgbouncer celery -A kennedy worker
beat: bin/start-pgbouncer celery -A kennedy beat