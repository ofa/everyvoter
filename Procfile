web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py kennedy.wsgi
beat: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A kennedy worker -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
worker: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A kennedy worker