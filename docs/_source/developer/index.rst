===============
Developer Guide
===============

EveryVoter is an open source platform released under a :doc:`MIT license </license>`. Pull requests can be made on the `Github repository`_.

EveryVoter is written in python using the Django framework. It’s setup to run using Python 2.7. EveryVoter’s front-end is based on Bootstrap 4, installed via the yarn package manager and compiled using gulp.


***************
Developer Setup
***************

Python Setup
============

For local development, run ``pip install -r dev-requirements.txt`` to pull python requirements.

After installing requirements but before running any migrations, you’ll want to create a `.env` file. The easiest way to do this is to duplicate and rename the :code:`.env-example` file to :code:`.env` and fill in the values with settings that matter.


While setting up EveryVoter you’ll need a free `Geocod.io`_ key. Put this API key in your new ``.env`` file before you go any further. With the exception of bulk testing user import functionality, during local development, it’s unlikely you’ll exceed Geocod.io’s free service plan.

The next step is to setup the database. Do this by running :code:``python manage.py migrate``

After static assets are compiled EveryVoter can then be run locally by running :code:`python manage.py runserver`

.. tip::
    By default, in :code:`DEBUG` mode, the default organization is what will be served at :code:`http://localhost:8000/`. If you add additional organizations, adding hostnames to your hosts file (:code:`/etc/hosts` on Mac) will let you test alternative organizations locally.

Front-End Setup
===============

To pull front-end requirements install ``yarn`` then run ``yarn install``

Compilation of front end code is done by running ``gulp prep``. This will compile static assets found in the ``/assets/`` folder, as well as all the modules found in ``/node_modules/``. These compiled assets will then be inserted into a new ``/dist/`` folder that is not tracked in git.

.. tip::
    ``gulp prep`` will also run a ‘watch’ command, monitoring for changes to static files. In Chrome you can use the `LiveReload Plugin`_ to monitor for changes and refresh the page after static files recompile.


Adding Initial Staff
====================

All staff members on EveryVoter are also constituents in their respective organization. While ``python manage.py runserver`` is active, visit ``https://localhost:8080/user/create/`` and create a new user.

There are 2 management commands needed to upgrade a constituent to a superuser and to set a password. As EveryVoter is organization-based, you’ll want to first promote your new constituent to a superuser by running ``python manage.py promote_superuser 1 email-you-used@email-domain.com`` then set a password by running ``python manage.py changepassword 1 email-you-used@email-domain.com``

After this has been done, you’ll be able to access the staff interface by visiting ``https://localhost:8080/manage/`` and Django administrative interface by visiting ``https://localhost:8080/manage/admin/``


*****************************
Contributor License Agreement
*****************************

Contributors to the OFA repository must sign the Contributor License Agreement (`Individual`_ or `Organization`_) before their submission can be accepted. For more information regarding EveryVoter’s CLA review the `Organizing for Action CLA FAQ`_.


.. _Github repository: https://github.com/ofa/everyvoter
.. _Geocod.io: https://www.geocod.io/
.. _LiveReload Plugin: https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei?hl=en
.. _Individual: https://ofa.github.io/cla-individual.html
.. _Organization: https://ofa.github.io/cla-entity.html
.. _Organizing for Action CLA FAQ: https://ofa.github.io/cla-faq.html
