web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py everyvoter.wsgi
beat: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q default -B --scheduler django_celery_beat.schedulers:DatabaseScheduler --without-heartbeat
worker: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority,bulk,default --without-heartbeat
worker_priority: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority,default --without-heartbeat