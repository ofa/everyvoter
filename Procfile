web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py kennedy.wsgi
beat: bin/start-pgbouncer newrelic-admin run-program celery -A kennedy worker -B
worker: bin/start-pgbouncer newrelic-admin run-program celery -A kennedy worker