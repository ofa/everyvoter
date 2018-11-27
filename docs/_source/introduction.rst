============
Introduction
============

******************
What is EveryVoter
******************


**EveryVoter** is an email automation platform that helps digital teams at organizations involved in voter outreach send customized, targeted “Get Out The Vote” emails at mass scale. Each email can contain its own specific messaging, drilling all the way down to the State House level.

Here’s an example: Let’s say, as a national organization, you want to send state- and district-specific emails on why voters should turn out this year (and who they should vote for).

This is what that EveryVoter email looks like for someone in Wisconsin’s 1st District.

.. image:: /_static/index/wi_example.png

The key to EveryVoter is in sending around election-related deadlines:

1) You select the deadlines you want to email around -- dates that could include Voter Registration deadlines, Early Voting or Absentee deadlines, and Election Day. EveryVoter continually monitors and updates these deadlines as states change them.
2) You write and pre-load HTML copy into the platform.
3) You track your emails as EveryVoter takes care of the rest at the right moment.

Your organization’s EveryVoter schedule, then, could look something like this:

- 7 Days Before Voter Reg Deadline
- 3 Days Before Voter Reg Deadline
- 0 Days Before Voter Reg Deadline


- 2 Months Before Election Day
- 1 Month Before Election Day
- 10 Days Before Election Day
- 7 Days Before Election Day
- 2 Days Before Election Day
- Election Day

**EveryVoter complements your existing email program by taking care of a large chunk of your GOTV email needs.**


************
Key Features
************

----------------------------
District-based customization
----------------------------

Emails are built using "Blocks", which are customized parts of EveryVoter sends that give each email a unique, personalized feel to a recipient living in a certain location.

EveryVoter supports message targeting to over 7000 political districts, on the state, congressional, state senate, and state house levels. Districts are referenced throughout EveryVoter using open source `Open Civic Data Identifiers`_ or OCD IDs.


--------------------------
Full email personalization
--------------------------

EveryVoter makes extensive use of the `Django Template Language`_, allowing personalization in nearly every component of an email.

Not only can email bodies, "From" addresses, and subject lines include the recipient's name, state, and election deadlines, it's also possible to customize messaging based on the election laws for individual states. An election-day template could include different messaging if a recipient's state supports same-day registration, or a voter registration email could contain different messaging if a recipient's state offers in-person early vote.


--------------
Built to scale
--------------

EveryVoter is built to contact millions of recipients in all 50 states and DC, with reasonable costs competitive with other email service providers. EveryVoter's fleet of mail servers can send hundreds of emails each second and can be configured to only launch when EveryVoter is delivering email. And by using Amazon's Simple Email Service for email delivery and tracking, alongside Heroku's per-second server billing, EveryVoter sends have a predictable per-email cost competitive with other email service providers.


------------------
Built-in Analytics
------------------

EveryVoter tracks opens, clicks, bounces, and unsubscribes for every email sent. And all links in EveryVoter emails have Google Analytics, Blue State Digital Tools, Action Network, Vote.org, and ActBlue sourcing information automatically appended, allowing easy tracking of the actions users take. Links to ActBlue even correctly pre-fill some of a constituent's contact information, reducing the steps needed to make a donation.


--------------------------
Multi-organization support
--------------------------

EveryVoter is built to be provided to multiple organizations under a Software as a service model. A group could launch a copy of EveryVoter and allow an unlimited number of organizations share the same server capacity and election deadline information. Each organization has their own email lists, email templates, datasets, and can even host EveryVoter on their own domain and use a custom name.

A collective could form to launch a common copy of EveryVoter, or a vendor could host and resell EveryVoter as a paid service.


.. _Django Template Language: https://docs.djangoproject.com/en/1.11/topics/templates/
.. _Open Civic Data Identifiers: https://opencivicdata.readthedocs.io/en/latest/ocdids.html
