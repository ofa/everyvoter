=========================
Super Administrator Guide
=========================

“Super Administrators” are users with unlimited global access to every organization on EveryVoter, as well as core functionality that keeps EveryVoter running. They’re able to do things like schedule send times, assign hostnames to organizations, add “sending” addresses that emails can be sent from, promote users to staff in all organizations, and edit details about elections.

Many Super Administrator tasks are done via the Django Admin, which is located at https://vote.your-domain.us/manage/admin/.

----------
Admin Home
----------

You start on the standard Django Admin.

.. thumbnail:: /_static/admin/admin_home.png

--------------------
Elections and States
--------------------

Super Administrators have the ability to edit both state and election information. These changes propagate immediately to all organizations on the platform.

.. note::
    2018 election and date details included in EveryVoter originally come from the `DNC Data Github Repository`_ and were then verified and updated by OFA staff. Be sure to verify all information prior to deploying EveryVoter into production, as states are constantly changing rules.

.. _DNC Data Github Repository: https://github.com/democrats/data

###########
List States
###########

.. thumbnail:: /_static/admin/admin_state_list.png


##################
Edit State Details
##################

.. thumbnail:: /_static/admin/admin_state_edit.png


##############
List Elections
##############

.. thumbnail:: /_static/admin/admin_elections.png


#############
Edit Election
#############

.. thumbnail:: /_static/admin/admin_elections_edit.png

.. note::
    When adding a new election, you'll need to provide one or more IDs for "Voting Districts." Voting districts are the value of the column ``id`` in the ``election_legislativedistrict`` table of EveryVoter's database of the districts where the election is happening. For example, Wisconsin's primary is held in the district ``ocd-division/country:us/state:wi``. If you search the ``election_legislativedistrict`` table in EveryVoter's database you'll see that this district has the ``id`` of ``6714``.
    This needs to be streamlined, but since elections are currently very rarely added it's a low priority.

-----------------
Sending Addresses
-----------------

Because Simple Email Server “whitelists” email addresses and domains that email can be sent from, it’s vital that the SES account associated with EveryVoter be authorized to send from every email address that emails can be sent from. To ensure this, adding “From” addresses are organization-specific.

“From” addresses can be made available to every organization in EveryVoter, or be associated with an individual organization. These email addresses or domains must be verified identities in SES before they’re added to EveryVoter. AWS provides information about `Verifying Identities in Amazon SES`_.

.. _Verifying Identities in Amazon SES: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-addresses-and-domains.html

###################
List Send Addresses
###################


.. thumbnail:: /_static/admin/admin_sendingemail_list.png


################
Add Send Address
################

.. note::
    Due to a peculiarity in the way EveryVoter creates the default sending address, the first new send address you add will fail and cause a 500 server error. Re-try to create that address. Every address added after that first address will be immediately added.

.. thumbnail:: /_static/admin/admin_sendingemail_add.png


-------
Domains
-------

EveryVoter supports multiple organizations using the system at the same time.

Currently, adding new organizations must be done using the Django command line. But once an organization is created, they can be served from multiple hostnames. For example, you may want an organization’s copy of EveryVoter to live at ``https://organization-name.common-name.us`` during setup. Then, once the organization has had a chance to add a CNAME, you can add ``https://vote.organization-domain.us/``.

Organizations always have a “Primary Domain.” This is the domain that EveryVoter should assume the organization is using for their production traffic. When emails are sent to constituents, the “Unsubscribe” and “Manage” links will point to pages on this domain.


######################
List Domains Addresses
######################

.. thumbnail:: /_static/admin/admin_domains_list.png


##########
Add Domain
##########

Hostnames can be added by clicking the “Add Domain” button on the top right of the domain list.

.. note::
    When adding a domain, remember to add the hostname to the ``ALLOWED_HOSTS`` environment variable. Otherwise Django will return an error on the new domain when ``DEBUG`` is not set to ``True``.

.. thumbnail:: /_static/admin/admin_domains_list.png


-----
Tasks
-----

EveryVoter is based around automated and scheduled activities, such as re-generating stats (every 10 minutes), sending staff notifications such as previews (once a day), and sending the emails themselves (once a day).

Scheduling tasks involve 2 steps:

1) Creating a “crontab” schedule (or a scheduled time of day or frequency) and
2) creating the task itself.


#########################
Listing Existing Crontabs
#########################

.. thumbnail:: /_static/admin/admin_scheduler_cronlist.png


####################
Creating New Crontab
####################

In this example, a new crontab sending at 1PM Eastern Time would be created.

.. thumbnail:: /_static/admin/admin_scheduler_cronadd.png


##################
Add Periodic Tasks
##################

When adding a periodic task, you'll need 3 bits of information

1) The task "name" -- This is a friendly name that's mostly for internal use. So you can keep track of your tasks in the admin.
2) The task name itself -- The ones we'll care about are all in the "Task (registered)" drop down
3) The schedule the task should run on, either an "Interval" or "Crontab" -- Mailing statistics calculation will be an interval, the rest are on a crontab

Other parts can generally be ignored.

.. thumbnail:: /_static/admin/admin_task_add.png


###############
Necessary Tasks
###############

EveryVoter has 3 necessary automated tasks. At a regular interval (10 minutes), mailing stats should be re-generated, once-a-day reports and notifications should be sent to staff, and once per day (usually in the morning), all emails should be sent from EveryVoter.

Trigger Mailings
================

| Task Name: Trigger mailings
| Task (registered): mailer.tasks.trigger_mailings
| Schedule: Daily, in the morning

.. thumbnail:: /_static/admin/admin_task_mailing.png


Calculate Mailing Statistics
============================

To significantly speed up the "Sent Mailings" interface, EveryVoter calculates stats such as "Clicks", "Opens", and "Unsubscribes" on a scheduled basis and stores the counts in the database. These counts what is displayed to staff when they login.

| Name: Trigger Stats Generation
| Task (registered): mailer.tasks.trigger_stats
| Schedule: Every 10 minutes

.. thumbnail:: /_static/admin/admin_task_stats.png


Trigger Notification: Daily Sample
==================================

| Name: Notifications: Daily Sample All
| Task (registered): notifications.tasks.daily_sample_batch
| Schedule: Daily, usually in the PM


.. thumbnail:: /_static/admin/admin_task_samples.png


------------------------
Democracy Works Consumer
------------------------

EveryVoter supports using the `Democracy Works Election API`_ as a source of election updates. If you provide an key and URL of the Democracy Works API EveryVoter can, on a regular schedule, search the Election API for elections that already exist in the EveryVoter platform and sync any updates to deadlines.

For example, If a state updates a deadline (such as expanding or changing early vote or voter registration deadlines) Democracy Works will update their API, and the next time EveryVoter queries the Democracy Works API the dates inside EveryVoter will update.

.. _Democracy Works Election API: https://www.democracy.works/elections-api/

##################
List API Responses
##################

Because the API is rate-limited, EveryVoter will only request from the API a maximum of one time per day. After the initial fetch, the data is stored in the database and viewable in the admin.

.. thumbnail:: /_static/admin/admin_democracy_responses.png

############
List Changes
############

.. thumbnail:: /_static/admin/admin_democracy_changes.png

#########################
Democracy Works API Tasks
#########################

Sync from Democracy Works
=========================

| Name: Sync from Democracy Works
| Task (registered): democracy_consumer.tasks.sync_elections
| Schedule: Daily, **after the "Trigger Mailing" task but before the "Daily Sample" task**

.. thumbnail:: /_static/admin/admin_task_democracy.png


Notify Admins of Democracy Works Changes
========================================

It's possible to send daily notifications of the most recent Democracy Works changes to EveryVoter users. In this case create a ``democracy_consumer.tasks.notify_changes`` scheduled task, with the 'Arguments' option including ``id`` for users who should be notified in the format ``[[1,2,3,4]]``. You can find this ID by looking at the ``id`` column in the ``accounts_user`` table for the intended recipients of the email.

| Name: Notify Democracy Works Changes
| Task (registered): democracy_consumer.tasks.notify_changes
| Schedule: Daily, **after Democracy Works changes**
| Arguments: ``[[1,4,12,300,...]]`` (IDs of admins to receive notifications)

.. thumbnail:: /_static/admin/admin_task_democracy_notify.png
