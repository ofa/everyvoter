===================
Management Commands
===================

There are 4 management commands available in the EveryVoter console that are useful for administration of EveryVoter.

-------------------
Create Organization
-------------------

Command: ``python manage.py create_organization``

To create an organization you’ll need to run the ``create_organization`` command. When running this command you’ll be entered into an interactive shell where you’ll be asked some specific questions around the organization being created.


-----------------
Promote Superuser
-----------------

Command: ``python manage.py promote_superuser {organization_id} {constituent_email}``

To promote a constituent to be a superuser, run the ``promote_superuser`` command. Since superusers are scoped by organization, you’ll need to provide the integer organization number when creating the command, as well as the email address. So to promote a superuser with the email address ``superuser@organization.us`` in organization 1, you’d run the command ``python manage.py promote_superuser 1 superuser@organization.us``

After performing this step you’ll need to provide an initial password by running the ``changepassword`` command.


-------------
Promote Staff
-------------

Command: ``python manage.py promote_staff {organization_id} {constituent_email}``

There are 2 ways to promote a constituent to staff, run the ``promote_staff`` command or go into the Django admin and mark that user as staff.

After performing this step you’ll need to provide an initial password for the new staff member by running the ``changepassword`` command.


---------------
Change Password
---------------

Command: ``python manage.py changepassword {organization_id} {constituent_email}``

This is a re-write of the existing “Change Password” functionality of Django to support multiple organizations. In this case, you’ll be asked to provide an organization id and the constituent’s email address.
