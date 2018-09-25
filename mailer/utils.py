"""Utilities for mailer"""
import re
import urlparse
import urllib

import newrelic.agent


# Regex for links in html
# pylint: disable=invalid-name
html_link_regex = re.compile(r"""href=["']([^\"\']*)["']""")


@newrelic.agent.function_trace()
def html_link_sourcer(html, user, source=None):
    """Source links in HTML"""
    email = user.email
    uuid = user.username
    first = user.first_name
    last = user.last_name

    def process_link(regex_result):
        """Process a link when found in the regex .sub()"""
        link = regex_result.group(1)
        parsed_link = urlparse.urlparse(link)

        query_data = urlparse.parse_qs(parsed_link.query)

        # Actblue uses refcode and refcode2 for source and sub-source. They
        # also allow you to pre-fill key fields in the donation forms by
        # passing that data in the querystring. We have easy access to name
        # and email, so we'll send that along.
        if parsed_link.hostname == 'secure.actblue.com':
            if 'refcode' not in query_data and source:
                query_data['refcode'] = [source]
            if 'refcode2' not in query_data:
                query_data['refcode2'] = [uuid]
            if 'email' not in query_data:
                query_data['email'] = [email]
            if 'firstname' not in query_data:
                query_data['firstname'] = [first]
            if 'lastname' not in query_data:
                query_data['lastname'] = [last]
        else:
            if 'source' not in query_data and source:
                query_data['source'] = [source]
            if 'utm_medium' not in query_data:
                query_data['utm_medium'] = ['email']
            if 'utm_source' not in query_data:
                query_data['utm_source'] = ['ev']
            if 'utm_campaign' not in query_data and source:
                query_data['utm_campaign'] = [source]

        # Vote.org needs 'campaign' in the querystring for campaign tracking
        if parsed_link.hostname and parsed_link.hostname.endswith(u'vote.org'):
            if 'campaign' not in query_data and source:
                query_data['campaign'] = [source]

        query_tuple = [(x, y) for x, y in query_data.iteritems() for y in y]

        parsed_link = parsed_link._replace(query=urllib.urlencode(query_tuple))
        replacement = u'href="{link}"'.format(link=parsed_link.geturl())
        return replacement

    return html_link_regex.sub(process_link, html)


def generate_source(email):
    """Generate a source code to be used in links inside an email"""
    return u"ev_{date}_{uuid}".format(
        date=email.created_at.strftime('%Y%m%d'),
        uuid=email.uuid)
