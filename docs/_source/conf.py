# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#

project = u'EveryVoter'
copyright = u'2018, Organizing for Action'
author = u'Organizing for Action'

extensions = [
    'sphinxcontrib.images',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'titles_only': False
}
html_static_path = ['_static']
htmlhelp_basename = 'EveryVoterdoc'
latex_documents = [
    (master_doc, 'EveryVoter.tex', u'EveryVoter Documentation',
     u'Organizing for Action', 'manual'),
]
man_pages = [
    (master_doc, 'everyvoter', u'EveryVoter Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'EveryVoter', u'EveryVoter Documentation',
     author, 'EveryVoter', 'One line description of project.',
     'Miscellaneous'),
]

def setup(app):
    app.add_object_type('confval', 'confval',
                        objname='configuration value',
                        indextemplate='pair: %s; configuration value')
