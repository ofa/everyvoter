web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py everyvoter.wsgi
beat: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q default,high_memory,feedback -B --scheduler django_celery_beat.schedulers:DatabaseScheduler --without-heartbeat
worker_high_memory: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority,bulk,default,feedback,user_import,high_memory --without-heartbeat
worker: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority,bulk,default,user_import,feedback --without-heartbeat
worker_priority: REMAP_SIGTERM=SIGQUIT newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority --without-heartbeat
