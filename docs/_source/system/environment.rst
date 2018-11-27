====================
Environment Settings
====================

EveryVoter configuration is done via environment variables, either in the app environment or in a .env file in the root directory of the project. Listed here are the environment variables used to configure EveryVoter.

`Django-environ`_ is used internally to manage settings. During development, these can be put into a ``.env`` file in your working directory. To get started with configuring a copy of EveryVoter with an ``.env`` file clone ``.env-example`` and use the filename ``.env``

.. _Django-environ: https://github.com/joke2k/django-environ

-----------------
Required Settings
-----------------

###############
Django Settings
###############


.. confval:: SECRET_KEY

**No Default Provided**

From the Django Documentation:

    A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

EveryVoter will refuse to start if ``SECRET_KEY`` is not set.


.. confval:: DATABASE_URL

**No Default Provided**

EveryVoter is optimized to work with PostgreSQL as the database backend on top of Heroku, with the database being provided by Heroku’s Postgres service.

In order to provide database service Heroku sets an environment variable called DATABASE_URL. The format is ``postgres://USER:PASSWORD@HOST:PORT/NAME``

For local development using `Postgres.app`_ we usually use ``DATABASE_URL=pgsql://@localhost/everyvoter``

.. _Postgres.app: https://postgresapp.com/


.. confval:: ALLOWED_HOSTS

**Default: [‘’] (Empty List)**

From the Django Documentation:

A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent an attacker from poisoning caches and triggering password reset emails with links to malicious hosts by submitting requests with a fake HTTP Host header, which is possible even under many seemingly-safe web server configurations.

Values in this list can be fully qualified names (e.g. 'www.example.com'), in which case they will be matched against the request’s Host header exactly (case-insensitive, not including port). A value beginning with a period can be used as a subdomain wildcard: '.example.com' will match example.com, www.example.com, and any other subdomain of example.com. A value of '*' will match anything; in this case, you are responsible to provide your own validation of the Host header.

Django also allows the fully qualified domain name (FQDN) of any entries. Some browsers include a trailing dot in the Host header which Django strips when performing host validation.


########
Geocoder
########


.. confval:: GEOCODIO_KEY

**No Default Provided**

An API key from the `Geocod.io`_ service. This is necessary to run EveryVoter. Accounts can be created quickly without a credit card, with approximately 1250 lookups per day included per API key.

.. _Geocod.io: https://geocod.io


-------------
Core Settings
-------------

These settings have presets


##########
EveryVoter
##########


.. confval:: DEFAULT_FROM_EMAIL

**Default: app@everyvoter.us (String)**

An email address you’re authorized to send to via SES that should be the default “From” address every organization can send from.

.. tip::
    It is very useful to set this prior to running your initial migrations.


######
Django
######


.. confval:: DEBUG

**Default: False**

If Django “Debug” mode should be on. Debug mode allows more detailed error pages to be shown, and will allow static images like stylesheets to be served by Django.

.. warning::
    Never deploy a site to the web with ``DEBUG`` set to ``True``. Doing so will likely expose private internal data to 3rd parties.


.. confval:: TIME_ZONE

**Default: US/Eastern (String)**

A string representing the time zone for this installation. It’s recommended that you choose from one of the following:

+---------------+-----------------+
| Timezone      | Name            |
+===============+=================+
| Eastern Time  | ``US/Eastern``  |
+---------------+-----------------+
| Central Time  | ``US/Central``  |
+---------------+-----------------+
| Mountain Time | ``US/Mountain`` |
+---------------+-----------------+
| Pacific Time  | ``US/Pacific``  |
+---------------+-----------------+


.. confval:: SESSION_COOKIE_NAME

**Default: everyvoter_sessionid**

Name of the cookie that stores the session ID.


.. confval:: CSRF_COOKIE_NAME

**Default: everyvoter_csrftoken**

Name of the cookie that stores the CSRF token.


.. confval:: SESSION_ENGINE

**Default: django.contrib.sessions.backends.cached_db**

Where sessions should be stored. You likely don’t need to change this.


.. confval:: SESSION_EXPIRE_AT_BROWSER_CLOSE

**Default: False**

If a user should be logged out of EveryVoter when they close their browser.


.. confval:: SESSION_COOKIE_AGE

**Default: 1 year (31536000 seconds)**

An integer number of seconds that sessions should stay active. This means the number of seconds before a user is automatically logged out.


#################
Celery/Task Queue
#################

EveryVoter relies on `Celery`_ as a distributed task queue and django-celery-beat for scheduled tasks.

.. _Celery: http://www.celeryproject.org/


.. confval:: BROKER_URL

**Default: pyamqp://guest@localhost//**


.. confval:: CLOUDAMQP_URL

**Default: None**

An alternative value for ``BROKER_URL``

In order to support the `CloudAMQP Heroku Addon`_, if ``CLOUDAMQP_URL`` is present in the environment, it overwrites ``BROKER_URL``

.. _CloudAMQP Heroku Addon: https://elements.heroku.com/addons/cloudamqp


.. confval:: CELERY_ALWAYS_EAGER

**Default: False (True if DEBUG is True)**

If Celery tasks should be immediately executed instead of put into a message queue. If DEBUG is true, this is also True and thus celery tasks are immediately executed.


.. confval:: CELERY_RESULT_BACKEND

**Default: django-db**

Where Celery results (usually success/failure messages) should be saved.

.. warning::
    It’s useful to store these in the database during testing, but in production, with production-level traffic, it’s highly recommended you change this to ``django-cache`` in order to store results in the Django cache and reduce hits to the database.


###################
Amazon Web Services
###################


Primary
=======

.. confval:: AWS_ACCESS_KEY_ID

**No Default Provided**

An AWS access key that has access to interact with files on S3 and send emails via SES.


.. confval:: AWS_SECRET_ACCESS_KEY

**No Default Provided**

The secret key associated with the ``AWS_ACCESS_KEY_ID`` above.


.. confval:: AWS_DEFAULT_REGION

**Default: us-east-1**


The AWS region that should be used.


AWS Simple Storage Service (S3)
===============================

EveryVoter uses Amazon S3 for storing both public and private files. “Public” files are items like stylesheets and logos, whereas “Private” files are items like previously uploaded user imports. By default, you’ll need two buckets, one for secure assets and one for public assets.


.. confval:: USE_S3

**Default: False**

Set to True if you wish to use S3 for static asset storage.


.. confval:: AWS_STORAGE_BUCKET_NAME

**Default: No Default Provided. Required if USE_S3 is True**

Name of the S3 bucket “public” files should be stored in.


.. confval:: DEFAULT_S3_PATH

**Default: "everyvoter/uploads"**

Path in the bucket that “Uploads” should be stored in. It’s highly recommended this setting be different between your staging and production environment if you’re sharing a single bucket for both.


.. confval:: STATIC_S3_PATH

**Default: "everyvoter/static"**

Similar to ``DEFAULT_S3_PATH`` above, the path that static assets should be stored in.


.. confval:: AWS_S3_CUSTOM_DOMAIN

**Default: No Default Provided**

If your “Public” S3 bucket has a web distribution at a different URL than normal, put it here. This is useful if you are serving your “Public” S3 bucket through a CDN.


.. confval:: AWS_PRIVATE_STORAGE_BUCKET_NAME

**Default: No Default Provided**

The “Private” S3 bucket that is not viewable by the public by default without an access token.


.. confval:: AWS_PRIVATE_STORAGE_EXPIRATION

**Default: 24 hours**

How long a “Secure Link” to a private S3 file should be valid for.


AWS Simple Email Service (SES)
==============================

EveryVoter relies on Amazon’s Simple Email Service for email sending. You’ll need an account with a high send rate before you run EveryVoter.


.. confval:: EMAIL_ACTIVE

**Default: False**

Set to ``True`` if EveryVoter should be sending emails. Without this being ``True`` EveryVoter’s internal mail infrastructure will be disabled and neither daily mailings nor samples will be sent.


.. confval:: SES_CONFIGURATIONSET_NAME

**Default: everyvoter**

The name of the SES “Configuration Set” that should be used. In SES, you set Configuration Sets to do things like choosing what type of reporting should be tracked (Opens, Clicks, Bounces, Complaints, etc) and where those notifications should be sent.

Configuration Sets will also let you have a custom “click” and “open” domain if you wish, so that when links are re-written for click tracking the links are through “click.your-domain.com.”


AWS Simple Notification Service (SNS)
=====================================

EveryVoter uses Amazon’s Simple Notification Service (SNS) to process feedback such as opens, clicks, bounces and complaints.


.. confval:: SES_FEEDBACK_TOPIC_ARN

**Default: None**

Enter the ARN of the SNS Topic attached to the SES Configuration Set you’re using for EveryVoter. The SNS verification process will be automatically responded to after this is set.


##########
Operations
##########

Hirefire
========

`HireFire`_ is a service that will scale your Heroku dynos based on usage. EveryVoter passes the length of RabbitMQ queues to HireFire.

.. _HireFire: https://www.hirefire.io/


.. confval:: HIREFIRE_TOKEN

**Default: No Default Provided**

An API token provided by HireFire.


.. confval:: HIREFIRE_QUEUES

**Default: All Celery queues in EveryVoter**

Using this environment variable you can overwrite the Celery queues HireFire should track by providing a list of queues, but it’s not recommended.


NewRelic
========

EveryVoter has extensive support for `NewRelic`_ and it's highly recommended you use NewRelic in your app.

.. _NewRelic: https://www.newrelic.com/


.. confval:: NEW_RELIC_LICENSE_KEY

**Default: None**

Your NewRelic API key


.. confval:: NEW_RELIC_APP_NAME

**Default: None**

The "App Name" in NewRelic. You’ll want to give EveryVoter an app name unique to each instance. For example, “EveryVoter - Staging” and “EveryVoter - Prod”


Heroku Buildpack - Python
=========================


.. confval:: DISABLE_COLLECTSTATIC

**No Default Provided**

**When first deploying to Heroku, you must set DISABLE_COLLECTSTATIC to "1" or compilation will fail.**


Heroku Buildpack - NGINX
========================

To speed up requests to EveryVoter each request is run through the NGINX web server on the Heroku dyno itself. This is done via the `Heroku Buildpack NGINX`_ buildpack.

.. _Heroku Buildpack NGINX: https://github.com/heroku/heroku-buildpack-nginx


.. confval:: USE_FIREWALL

**Default: false**

If set to true only requests from IP addresses owned by Cloudflare or Fastly will be accepted. If you fork EveryVoter you can edit the file ``/config/nginx-httpaccess.conf.erb`` to whitelist whichever IP ranges you wish when the firewall is turned on.


Heroku Buildpack - PgBouncer
============================

EveryVoter by default uses `PgBouncer`_ to reduce the latency during the database connect and disconnect step during each request. PGBouncer also serves to reduce the number of simultaneous connections on the database server itself. This is done via the `Heroku buildpack pgbouncer`_ buildpack.

.. _PgBouncer: https://wiki.postgresql.org/wiki/PgBouncer
.. _Heroku Buildpack pgbouncer: https://github.com/heroku/heroku-buildpack-pgbouncer


.. confval:: PGBOUNCER_LOG_CONNECTIONS

**Default: 1**

If set to 1 you’ll see database connections for each request in your Heroku log. It’s a lot of crosstalk you likely don’t need. Set this to 0 to keep logs simpler.


.. confval:: PGBOUNCER_LOG_DISCONNECTIONS

**Default: 1**

Similar to ``PGBOUNCER_LOG_CONNECTIONS``

.. note::
    You'll notice your logs filling up quickly if you don't change this and ``PGBOUNCER_LOG_CONNECTIONS`` to ``0``
