web: bin/start-pgbouncer bin/start-nginx newrelic-admin run-program gunicorn -k gevent -c config/gunicorn_config.py everyvoter.wsgi
beat: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q default,high_memory -B --scheduler django_celery_beat.schedulers:DatabaseScheduler --without-heartbeat --concurrency 4
worker_high_memory: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q high_memory --without-heartbeat --concurrency 4
worker_primary: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority,bulk,default,feedback,user_import --without-heartbeat
worker_general: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q bulk,default,feedback --without-heartbeat
worker_import: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q user_import --without-heartbeat
worker_priority: REMAP_SIGTERM=SIGQUIT bin/start-pgbouncer newrelic-admin run-program celery -A everyvoter worker -Q bulk_priority --without-heartbeat --concurrency 14
