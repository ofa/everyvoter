=================================
Amazon Web Services Configuration
=================================

EveryVoter relies heavily on 1) SES for email sending, 2) S3 for static file storage, and 3) SNS for feedback (bounce, open, click, etc) processing. The AWS credentials your copy of EveryVoter is configured to use should have access to all of these AWS services to operate.

---------------------------
Simple Storage Service (S3)
---------------------------

When setting up S3 EveryVoter requires 2 buckets. One to store secure assets (that does not need a website distribution) and one that does support website distribution to store publicly accessible static assets.

----------------------------
Simple Email Service and SNS
----------------------------

EveryVoter uses SES for email sending and SNS for feedback processing.

-------------------
Email Sending (SES)
-------------------

Amazon provides extensive `SES Setup Documentation`_. Before an email is added to EveryVoter the address (or domain) needs to be whitelisted to be sent from in SES.

It’s possible to run multiple copies of EveryVoter on one AWS account, but still keep emails separated, by having separate “Configuration Sets” which emails can be routed to. For example, you may have an “everyvoter-prod” Configuration Set for production traffic and “everyvoter-staging” for staging emails. Configuration Sets are scoped to the full install of the EveryVoter platform and can be set by changing the environment variable ``SES_CONFIGURATIONSET_NAME``

Multiple copies of EveryVoter can share a common Configuration Set, as long as they have separate ``APP_NAME`` environment variables. However, this will likely result in unnecessary traffic to EveryVoter.

.. warning::
    There is not currently a rate limiting functionality in EveryVoter, so your send rate should be sufficiently high or you should limit the number of Heroku dynos allocated to email sending.

.. _SES Setup Documentation: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/setting-up-email.html

------------------------
Feedback Reporting (SNS)
------------------------

Displaying and processing feedback (bounces, spam complaints, opens and clicks) is a vital part of EveryVoter. Feedback processing is done in real time using SNS.

Amazon provides documentation on setting up SNS feedback in their documentation. The ARN of your SNS topic should be inserted as the ``SES_FEEDBACK_TOPIC_ARN`` configuration variable.

SNS should be set to use the HTTPS endpoint https://vote.your-domain.us/feedback/email/ . If ``SES_FEEDBACK_TOPIC_ARN`` matches the ARN of the SES topic EveryVoter will immediately authorize further traffic.

Only send ``Bounce``, ``Complaint``, ``Open``, and ``Click`` feedback to EveryVoter.

Other types of feedback will be immediately discarded and may cause unnecessary load on EveryVoter’s web servers.
