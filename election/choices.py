"""Choices for models in Election App"""
DISTRICT_TYPES = (
    ('state', 'State'),
    ('cd', 'Congressional District'),
    ('stateleg_upper', 'State Senate/Upper State'),
    ('stateleg_lower', 'State Rep/Lower State'),
)


ELECTION_TYPES = (
    ('primary', 'Federal Primary'),
    ('general', 'Federal General'),
    ('special', 'Federal Special')
)


DEADLINES = (
    ('registration', 'Registration'),
    ('evip_start_date', 'Early Vote Start'),
    ('evip_close_date', 'Early Vote End'),
    ('vbm_application_deadline', 'Vote By Mail Applications Due'),
    ('vbm_return_date', 'Vote By Mail Returns Due'),
    ('election_date', 'Election Day')
)


# From https://github.com/democrats/election-calendar
STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
    #('AS', 'American Samoa'),
    ('DC', 'District of Columbia')#,
    #('FM', 'Federated States of Micronesia'),
    #('GU', 'Guam'),
    #('MH', 'Marshall Islands'),
    #('MP', 'Northern Mariana Islands'),
    #('PW', 'Palau'),
    #('PR', 'Puerto Rico'),
    #('VI', 'Virgin Islands')
)
