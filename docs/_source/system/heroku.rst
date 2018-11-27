====================
Heroku Configuration
====================

EveryVoter is built to run on Heroku.

----------
Deployment
----------

Initial deployment can be done by creating a new Heroku app, setting the buildpack of the new app to ``https://github.com/heroku/heroku-buildpack-multi``, adding the relevant add-ons, setting the environment variable ``DISABLE_COLLECTSTATIC`` to ``1``, and pushing code to the new app using git.

.. warning::
    If you do not set ``DISABLE_COLLECTSTATIC`` to ``1`` on Heroku, your slug will fail to compile.

During a push, both static assets and python requirements will be loaded into the Heroku slug. However, static assets will not be deployed. You run these inside the Heroku shell.

After this point, you’ll want to set all the environment variables necessary to run EveryVoter. This includes configuring AWS and Geocod.io.

The final step to get a functioning EveryVoter running is to run the management command `python manage.py migrate` to setup the Postgres database.

Tip: There are two ways to run python commands on Heroku, both via ``heroku run``. If you wish to run commands one-at-a-time, use the command ``heroku run -a your-app-name {command}`` on your local machine. If you wish to drop into a shell in your production environment enter the command ``heroku run -a your-heroku-app-name bash``.

When in the bash on out you can run ``python manage.py`` commands (or ``./manage.py``) or static compilation steps like ``yarn`` and ``gulp``.

##########
Buildpacks
##########

EveryVoter stores its buildpack configuration in the ``.buildpacks`` file and uses the `Heroku Buildpack Multi`_ buildpack to pull these buildpacks during the build process, so you can set your buildpack to ``https://github.com/heroku/heroku-buildpack-multi`` during setup.

.. _Heroku Buildpack Multi: https://github.com/heroku/heroku-buildpack-multi


######
Addons
######

It’s recommended that for production applications you have a RabbitMQ add-on (EveryVoter is setup to work with `CloudAMQP`_ with a dedicated plan recommended for production purposes), a paid memcached addon (EveryVoter is setup to work with a paid `Memcachier`_ plan), and a `Heroku Postgres`_ installation.

.. note::
    Picking the right Heroku Postgres plan is vital, and it’s useful to review the performance characteristics of various plans. It’s highly recommended you have a Heroku Postgresql plan with a larger connection limit (Standard 2 or higher) and depending on the scale and desired to send speed a larger number of PIOPS (Standard 3 or higher.)

If you do not otherwise have a `New Relic`_ license it’s very highly recommended you purchase this add-on as well.

.. _CloudAMQP: https://elements.heroku.com/addons/cloudamqp
.. _Memcachier: https://elements.heroku.com/addons/memcachier
.. _Heroku Postgres: https://elements.heroku.com/addons/heroku-postgresql
.. _New Relic: https://elements.heroku.com/addons/newrelic


##########
Dyno Types
##########

There are currently 7 dyno types on EveryVoter. It’s recommended operators of EveryVoter always have one or two ``web``, one ``beat``, and one ``worker_primary`` dyno running at all times. The other dynos can be scaled as needed manually or via HireFire.

1) ``web`` - Webservers. EveryVoter traditionally has limited traffic, with the biggest source of incoming traffic being email feedback. In general, this can be 1 or 2 1X dynos.
2) ``beat`` - Scheduler and general worker. This dyno triggers scheduled tasks, as well as serves as a general and constituent import worker. There should never be more than one ``beat`` dyno running, and it should always run. This is a 2X dyno, similar to ``worker_high_memory``
3) ``worker_high_memory`` - This is a worker dyno that handles requests that require more memory than normal, like processing large import files. This dyno is not regularly needed and can be kept at 0 unless the ``high_memory`` queue grows too large for the ``beat`` worker to consume. These are 2X dynos.
4) ``worker_primary`` - This is a general worker that is configured to handle all tasks that do not require extra memory, and is also configured to process user imports. It’s recommended that you only ever have one ``worker_primary`` running. This is a 1X dyno.
5) ``worker_general`` - This is a general worker that accepts all tasks that do not require 2X memory, with the exception of constituent imports. This can be scaled as needed. These are 1X dynos.
6) ``worker_import`` - These dynos handle constituent imports. As geocod.io sometimes limits the rate of imports, and because the import process can be database intensive, it’s recommended that you scale these only when the ``user_import`` queue gets large, and you should only scale this to one or two extra dynos. These are 1X dynos.
7) ``worker_priority`` - These 2X dynos handle bulk email sending, and should be scaled up to speed the send process during the daily send. They can be set at 0 by default and scaled by HireFire. These are 2X dynos.

.. warning::
    By default, Heroku restarts all dynos once per day, 24 hours and up to 216 minutes after the previous restart. When Heroku tells a dyno to shutdown, it has 30 seconds to do so.

    Some tasks in EveryVoter take longer than 30 seconds to complete. If you find yourself regularly doing releases within 216 minutes of the time your app sends daily messages, do a ``heroku ps:restart beat`` a few hours after your release (in the evening.) Splitting out tasks so they never persist longer than 60 seconds is on the EveryVoter roadmap and may be a reason to use a service other than Heroku if using EveryVoter for a long time.


--------
HireFire
--------

A key feature of Heroku is the ability to scale to (by default) up to 100 dynos at a time within seconds. During the email send process a sizable amount of compute resource is needed.

`HireFire`_ provides an automated way to increase or decrease the number of dynos your application has provisioned based on the length of various RabbitMQ queues.

In EveryVoter the HireFire endpoint is located at ``https://everyvoter.yourdomain.us/hirefire/{hirefire ID}/``.

By default EveryVoter provides the length of the following queues:

1) ``default`` - General tasks that can be run on 1X dynos. Usually things such as email sampling
2) ``bulk`` - The number of general tasks that can be run at a relatively low pace.
3) ``bulk_priority`` - The number of emails left to be sent.
4) ``user_import`` - Number of pending user import operations.
5) ``high_memory`` - Tasks that require 2X dynos, such as triggers for emails.
6) ``feedback`` - Feedback from Amazon SES.

.. _HireFire: https://www.hirefire.io
