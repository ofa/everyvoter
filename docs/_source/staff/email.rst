=====
Email
=====

**Sends** refer to the individual emails that go out from EveryVoter. For example, if your organization is sending Election Day reminders to CA, KY, IL, and FL on the same day, you have **four sends** on that day.

On your organization's EveryVoter main page, you can see a list of all upcoming sends for that week. By clicking the “All” link in parentheses next to “Upcoming Sends,” you can see a fuller list of every upcoming send you have scheduled in EveryVoter.

.. contents::
    :local:
    :depth: 1

---------
Templates
---------

Each send is made up of a **template**. Templates exist in EveryVoter as the building block of an email, providing HTML style and copy that will be replicated in every send for that deadline.

When EveryVoter sends emails all fields **except "Pre-Header Text"** are treated as Django templates and allow :ref:`conditional content and fields <concepts-templates>`.

Your organization may, for example, have a template for “7 Days Pre-Voter Registration Deadline.” This template will have generic language -- along with space for customized dataset entries like [STATE] and customized full blocks.

.. contents::
    :local:
    :depth: 1

##############
List Templates
##############

.. thumbnail:: /_static/manage/manage_templates_list.png

########################
Edit Individual Template
########################

On the Existing Templates page, you can see all of the templates your organization has added to EveryVoter. By clicking “Preview,” you can see that template exactly as it would appear to a recipient of the email. By clicking “Delete,” you can remove it from your template library.

By clicking “Update,” you can edit one of your existing individual templates. Here are the things you’ll be able to edit once you open up an individual template to update:

- The name of the template (e.g., PRIMARY Election Day [2 Day Reminder])
- Election Type (e.g., Federal Primary, Federal General)
- Days to Deadline
- “From Name” (who will show up as the sender of the email)
- Subject Line
- Pre-Header Text
- HTML Email Body

.. warning::
    EveryVoter does not support conditional content or custom fields within Pre-Header Text. Conditional content and fields are allowed in the "From Name", "Subject Line", the "HTML Email Body", as well as all blocks, wrappers.

.. thumbnail:: /_static/manage/manage_templates_edit.png


Choosing Blocks to Include
==========================

**Blocks** are the customized parts of your EveryVoter sends that give each email a unique, personalized feel to a recipient living in a certain location.

Inside each email, leave a spot for each block -- for example, the WI-01 House Block:

    **We can replace Speaker Ryan**, who has advanced the Trump agenda at every turn, with a representative who will stand up for hard-working Wisconsin families.

This block is inserted into every email that goes to WI-01, at your desired spot in the send -- and it only goes to those recipients who live in WI-01, while someone in CA-49 would get a separate message in this place specific to the CA-49 House race.

.. thumbnail:: /_static/manage/manage_templates_edit_blocks.png


#################
Preview Templates
#################

**Previewing** a template allows you to see a sample of the email, with all of the personalization that will be delivered to inboxes.

All previews must have an election. If you wish to preview what a constituent in a specific district will see, you can enter comma-separated OCD-IDs on the preview page as well.

Preview Template Without Blocks
===============================

If you’d like to preview without a block, you just need to choose an election. If you’d like to sample a template to an email address, enter the email address in the “Sample Email” box.

.. thumbnail:: /_static/manage/manage_templates_preview-noblocks.png


Preview Templates Sent to Individual Districts
==============================================

If you’d like to preview what an email will look like when sent to users in an individual district including blocks targeted to their district, enter the OCD IDs of the districts you’d like to preview in the “OCD IDs” box on the right. These should be comma separated.

.. thumbnail:: /_static/manage/manage_templates_preview-blocks.png


-----------------
Upcoming Mailings
-----------------

The Upcoming Mailings tab allows you to see all of the emails that are scheduled to be delivered, sorted by date, and the number of recipients who will receive them.

You can see more information about a specific mailing by clicking on the Election.

.. thumbnail:: /_static/manage/manage_upcomingmailings.png

-------------
Sent Mailings
-------------

The **Sent Mailings** tab details all of the emails that have been delivered.

On this page, you can view the date that the mailing was sent, the name of the template of the mailing, the deadline tied to that template, and the specific election.

Also on this page are statistics about each mailing, including the number of recipients (Sent), whether or not the mailings was successfully delivered (Status), and the clicks, opens, and list unsubscribes.

.. thumbnail:: /_static/manage/manage_sentmailings_list.png

----------------
Mailing Wrappers
----------------

“Wrappers” are pieces of HTML that surround every template. These will contain things like your organization’s logo, address, and unsubscribe URL.

A simple default wrapper is included with EveryVoter.

#############
List Wrappers
#############

.. thumbnail:: /_static/manage/manage_wrapper_list.png

############
Edit Wrapper
############

A good **wrapper** communicates information that you want to be included on every email that EveryVoter delivers.

It shouldn’t contain anything will interfere or take away from the content of your mailing.

.. thumbnail:: /_static/manage/manage_wrapper.png

Important Fields
================

All template fields that are available inside of templates are available inside of wrappers. Three are especially important. Those are:

1) Pre-Header tag ``{{ pre_header }}`` immediately after the first <body> tag in your header
2) The “update your information” tag ``{{ manage_url }}``, and
3) The “unsubscribe” tag ``{{ unsubscribe_url }}``
