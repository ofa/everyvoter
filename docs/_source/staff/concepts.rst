===================
EveryVoter Concepts
===================


.. _concepts-datasets-blocks:

-------------------
Datasets and Blocks
-------------------

When telling recipients who to vote for, EveryVoter takes inspiration from Legos. Organizations provide EveryVoter "blocks" of messaging, with each block associated with a legislative district and a ranking of its importance. When EveryVoter needs to send an email, it treats building the email like building a Lego tower, finding the blocks that match to the legislative districts the recipient lives in and stacking them based on their importance.

For example, you may create a block targeted to Nevada's 3rd congressional district telling the recipient to vote for Susie Lee, whereas you may create a different block targeted to Minnesota's 2nd district telling the recipient to vote for Dean Phillips. When EveryVoter sends an email to a recipient in Nevada's 3rd district, it will add the Susie Lee block to the recipient's email, and when it sends an email to a recipient in Minnesota's 2nd district, it will include the Dean Phillips block.


.. _concepts-ocdid:

-----------------------------
Open Civic Data IDs (OCD IDs)
-----------------------------

`Open Civic Data Identifiers`_ (OCD IDs) are a common way of identifying specific legislature districts or states. EveryVoter uses OCD IDs to ensure your organization’s emails are sent to the correct audience.

When uploading a dataset, the EveryVoter user should match the proper District ID is associated next to it (e.g., CA-49 should have the OCD ID: ``ocd-division/country:us/state:ca/cd:49``).


.. _concepts-templates:

---------------------------------
Conditional Content and Templates
---------------------------------

Similar to other mailers, EveryVoter allows organizations to send emails with “conditional content.” Conditional content is content that is specific to the recipient, election, location or otherwise contained inside a dataset. This content can either be inserted directly into the template or perform more complex operations such as format a date in a specific format.

EveryVoter relies heavily on the Django Template Engine for conditional content. Each email sent is treated by EveryVoter as if it is a page being visited by a user in their web browser, so whatever works in Django templates on the web generally works inside of EveryVoter templates, dataset blocks, and wrappers.

EveryVoter is based on the Django 1.11 template engine.

For details about available default fields, review the “Built in Template Tags and Filters” page in the `Django Documentation`_.

For details about working with dates, in particular, review the documentation about the `Django date filter`_.

.. warning:: EveryVoter will attempt to prevent the saving of templates with syntax errors, but always preview your content before the next scheduled mailing.

.. _concepts-fields:

###########################
Available EveryVoter Fields
###########################

The following fields are available to be inserted in mailing templates, wrappers, and blocks.

.. contents::
    :local:
    :depth: 1


Recipient
#########

Fields specific to the recipient of the email. To insert the user’s first name with the backup “Friend,” use `{{ recipient.first_name|default:”Friend” }}`

Note: During previews, the “Recipient” is always the staff member who is logged in requesting the preview.

| ``{{ recipient.first_name }}`` - Constituent’s First Name
| ``{{ recipient.last_name }}`` - Constituent’s Last Name
| ``{{ recipient.email }}`` - Constituent’s Email Address
| ``{{ unsubscribe_url }}`` - URL the constituent can visit to unsubscribe from EveryVoter
| ``{{ manage_url }}`` - URL the constituent can visit to update their name or location


Organization
############

Fields specific to the organization sending the email.

| ``{{ organization.name }}`` - Name of the organization
| ``{{ organization.homepage }}`` - Homepage of the organization
| ``{{ organization.privacy_url }}`` - URL of the privacy policy of the organization
| ``{{ organization.terms_url }}`` - URL of the terms of service for the organization
| ``{{ organization.url }}`` - URL of organization’s copy of EveryVoter
| ``{{ organization.from_address }}`` - Email address (info@yourdomain.com) the email is sent from


Email and Template
##################

Fields specific to the email being sent. These will be blank in wrapper or block previews.

| ``{{ email.pre_header }}`` - What appears in the HTML (use {{ pre_header }} after the first <body> in wrappers, this will insert the correctly hidden version)
| ``{{ email.subject }}`` - Subject line of email
| ``{{ template.name }}`` - Internal name of template
| ``{{ template.deadline_type }}`` - Type of deadline (possible values `vr_deadline`, `evip_start_date`, `evip_close_date`, `vbm_application_deadline`, `vbm_return_date`, `election_date`)
| ``{{ template.get_deadline_type_display }}`` - “User Friendly” version of deadline type (possible values `Registration`, `Early Vote Start`, `Early Vote End`, `Vote By Mail Applications Due`, `Vote By Mail Returns Due`, `Election Day`)


Election
########

Fields specific to the election the email is related to.

To use Election Date in the format “Day of Week, Month Day,” use the code `{{ election.election_date|date:"l, F j" }}`

.. warning:: These dates may change over time as states change their deadlines. It’s recommended you always caveat emails telling users to check with their local election officials.

| ``{{ election.election_date }}`` - Date of the election (`Date` object, review Django’s template documentation on how to format dates)
| ``{{ election.vr_deadline }}`` - The deadline by which voters in the state must register to vote (Either blank for states with no deadline or a `Date` object)
| ``{{ election.vr_deadline_online }}`` - The explicit deadline by which voters in the state must register to vote online in order to vote (Either blank or a `Date` object)
| ``{{ election.evip_start_date }}`` - The date in which early voting in person begins in the state (Blank or a `Date` object)
| ``{{ election.evip_close_date }}`` - The date that early voting in person ends in the state (Blank or `Date`)
| ``{{ election.vbm_application_deadline }}`` - the date by which voters must return their applications applying to vote by mail (Blank or `Date`)
| ``{{ election.vbm_return_date }}`` - The date by which voters must return their mailed ballots (Blank or `Date`)


State
#####

Fields specific to the state an election is happening in (and the constituent lives in).

.. warning:: These may change over time. It’s recommended you always caveat emails telling users to check with their local election officials.

| ``{{ state.code }}`` - State Code, IL, WI, NM, etc
| ``{{ state.name }}`` - Name of state
| ``{{ state.demonym }}`` - Demonym of residents of state
| ``{{ state.is_state }}`` - Is state or not, currently True for all locations except Washington DC (True/False, to be used in templates as `{% if state.field %}True{% else %}False{% endif %}`)
| ``{{ state.senate_2018 }}`` - Whether at least 1 U.S. Senate seat in the state will appear on the general election ballot (True/False)
| ``{{ state.governor_2018 }}`` - Whether the state's Governor's seat will appear on the general election ballot (True/False)
| ``{{ state.has_vr }}`` - Whether the state registers voters (North Dakota doesn't) (True/False)
| ``{{ state.automatic_vr }}`` - Whether the state offers automatic voter registration
| ``{{ state.online_vr }}`` - Whether the state offers online voter registration
| ``{{ state.same_day_vr }}`` - Whether the state offers same day voter registration, defined here as the ability to register to vote and also cast a vote prior to election day
| ``{{ state.eday_vr }}`` - Whether the state offers election day voter registration, defined here as the ability to register to vote and also cast a vote on election day
| ``{{ state.early_vote_in_person }}`` - Whether the state offers some form of voting prior to election day via a personal appearance
| ``{{ state.in_person_absentee }}`` - Whether the only form of voting prior to election day via personal appearance is at a single location per jurisdiction
| ``{{ state.early_vote_by_mail }}`` - Whether the state allows for voting by mail prior to election day
| ``{{ state.early_vote_by_mail_fault }}`` - Whether there are restrictions as to who can vote by mail prior to election day
| ``{{ state.early_vote_by_county }}`` - Whether the availability or dates of early votes is county-by-county
| ``{{ state.perm_absentee }}`` - Whether the state offers a permanent absentee option in which a voter can either elect (or will automatically receive) a mail ballot
| ``{{ state.election_calendar_url }}`` - URL of an official 2018 election calendar



.. _Open Civic Data Identifiers: https://opencivicdata.readthedocs.io/en/latest/ocdids.html
.. _Django Documentation: https://docs.djangoproject.com/en/1.11/ref/templates/builtins/
.. _Django date filter: https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#date
