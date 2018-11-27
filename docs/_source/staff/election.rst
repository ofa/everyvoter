=========
Elections
=========

EveryVoter sets the timing of mailings around Elections. Elections in EveryVoter have two components:

1) Things that you can control, like if you’ll be sending around a specific deadline in a state, and
2) Things that you cannot control, such as deadlines in specific states.

Because election laws are nearly always state-specific, EveryVoter elections are never larger than a specific state. So instead of one election happening on November 6th, 51 elections are happening on November 6th.

.. contents::
    :local:
    :depth: 2

---------
Elections
---------

##############
List Elections
##############

.. thumbnail:: /_static/manage/manage_election_list.png

#################################
View and Edit Individual Election
#################################

Organizations are able to toggle what types of notifications each election should have, as well as see past and upcoming mailings related to that election.

It’s also possible to disable certain types of emails (such as Voter Registration emails to states that require an excuse to vote) in the Organizing Settings page.

.. thumbnail:: /_static/manage/manage_election_detail.png


-------------------
Datasets and Blocks
-------------------

Datasets are the information basis for all of the personalized information that is plugged into mailings in EveryVoter.

For more details about the concept behind datasets and blocks, see the Dataset and Blocks section of :ref:`EveryVoter Concepts <concepts-datasets-blocks>`

Datasets are comprised of 3 items: **Blocks**, **fields**, and district-specific **values**.

**Blocks** are snippets of code that can be inserted into emails when a constituent lives in a district defined within the dataset.

Fields and values can be best described as being similar to a spreadsheet. **Fields** are the column names, each row is a district signified by an :ref:`OCD ID <concepts-ocdid>`, and each individual cells is a **value** that is associated with a field (column) and district (row.)

For example, you could have a dataset called “Representatives Dataset.” A field (column name) in this dataset could be called ``twitter_handle``, a row could be ``ocd-division/country:us/state:ca/cd:10``, and the cell value could be ``@RepJeffDenham``.

Inside a block in this, you could use the merge-field ``{{ dataset.twitter_handle }}`` -- and any constituent living in the district ``ocd-division/country:us/state:ca/cd:10`` who sees a block contained within the “Representatives Dataset” would see ``@RepJeffDenham`` whenever a block has the code ``{{ dataset.twitter_handle }}``

Datasets can be uploaded via CSV, with the first column being the OCD ID and each column theirafter being the field name.

.. warning::
    :ref:`Conditional content and fields <concepts-templates>` are allowed in blocks but are not allowed within the values of datasets.


#############
List Datasets
#############

.. thumbnail:: /_static/manage/manage_dataset_list.png

############
View Dataset
############

.. thumbnail:: /_static/manage/manage_dataset_detail.png

#########################
Dataset Fields and Values
#########################


List of fields
==============

.. thumbnail:: /_static/manage/manage_dataset_valuelist.png

View and Edit Individual Values
===============================

.. thumbnail:: /_static/manage/manage_dataset_value.png

##########
Edit Block
##########

**Blocks** are the custom snippets of code held within a dataset. They’re shown if the block is targeted to an email, and the dataset is targeting to a constituent’s district

For example, if you’d like to include custom messaging about a representative’s vote, and deliver that messaging 5 days before Election Day, you would create a block for that vote.

In addition to values from the dataset, blocks also have access to all the same fields that are available inside templates (such as ``{{ election.election_date }}`` and ``{{ state.code }}``)


Here is an example block that includes conditional content as well as multiple dataset values:

.. code-block:: html

    We can {% if state.code == 'DC' %}hold accountable a Republican government
    {% else %} replace a Republican-controlled House{% endif %} that handed
    the wealthiest 1% of {{ dataset.state_demonym_plural }} a tax break of
    {{ dataset.state_tax_break }} each, and voted for a bill that would have
    stripped health care from {{ dataset.state_healthcare }}
    {{ dataset.state_state }} residents.

In this example, since the field ``state.code`` is available within blocks, and since DC is not represented by a voting member of the house, we use a ``{% if state.code == 'DC' %}`` statement to detect instances where the block is being sent to DC and provide custom content.

.. tip::
    All the :ref:`fields available in email templates and wrappers <concepts-fields>` are open in blocks.


.. thumbnail:: /_static/manage/manage_block_edit.png


#############
Preview Block
#############

.. thumbnail:: /_static/manage/manage_block_preview.png


###########
List Blocks
###########

It's possible to list all blocks in all datasets.

.. thumbnail:: /_static/manage/manage_blocks_list.png


----------
Categories
----------

It's currently possible to "Tag" blocks and datasets by assigning them categories. This is a work in progress.

#######################
List Dataset Categories
#######################

.. thumbnail:: /_static/manage/manage_datasets_categories.png

#####################
List Block Categories
#####################

.. thumbnail:: /_static/manage/manage_blocks_categories.png
