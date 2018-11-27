======================
Geocoder Configuration
======================

EveryVoter relies on `Geocod.io`_ for geocoding. Geocod.io was chosen because of their reasonable price and support for the 2019 Pennsylvania congressional districts.

EveryVoter takes responses from Geocod.io and turns them into :ref:`Open Civic Data IDs <concepts-ocdid>` which are then stored in the database. To reduce the number of queries sent to Geocod.io (as requests to Geocod.io both slow down importing as well as have a monetary cost) geocode responses are stored in the database and queried during the user addition process.

Once you have a Geocod.io API key, insert it as the ``GEOCODIO_KEY`` environment variable.

.. _Geocod.io: https://geocod.io
