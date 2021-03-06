"""Render an email"""
from email.utils import formataddr

from django.core.cache import cache
from django.template import Context, Template
from django.utils.safestring import mark_safe
import newrelic.agent

from accounts.models import User
from blocks.compose_blocks import compose_blocks
from blocks.models import Block
from election.models import OrganizationElection, LegislativeDistrict
from mailer.models import Email
from mailer.utils import html_link_sourcer, generate_source


@newrelic.agent.function_trace()
def get_email(email_id):
    """Get the email using all the relevant select_relateds"""
    key = 'get-email-key{email_id}'.format(email_id=email_id)
    email = cache.get(key)
    if not email:
        email = Email.objects.select_related(
            'mailing',
            'mailingtemplate',
            'mailing__template',
            'mailing__organization_election',
            'mailing__organization_election__election',
            'mailing__organization_election__election__state',
            'mailing__organization_election__email_wrapper').get(id=email_id)

        # If the email is a `mailing` add it to the cache
        if hasattr(email, 'mailing'):
            cache.set(key, email)

    return email


@newrelic.agent.function_trace()
def get_email_context(user_id,
                      email_id=None,
                      election_id=None):
    """Get context for an email

    Get the context used for emails

    Args:
        user_id: id of the User
        email_id: id of the Email
        election_id: Id of the Election (optional, required if Email is not a
                     Mailing object or is missing)
    """
    # Start pulling from the database all the context we need
    user = User.objects.select_related(
        'organization', 'organization__primary_domain',
        'organization__from_address', 'location').get(pk=user_id)
    organization = user.organization

    newrelic.agent.add_custom_parameter(
        'organization_id', organization.pk)
    newrelic.agent.add_custom_parameter(
        'email_id', email_id)
    newrelic.agent.add_custom_parameter(
        'recipient_id', user_id)

    if email_id:
        email = get_email(email_id)
        manage_url = user.manage_url(email)
        unsubscribe_url = user.unsubscribe_url(email)
    else:
        # We may need email-less context for situations such as block and
        # wrapper previews.
        email = None
        manage_url = ''
        unsubscribe_url = ''

    if email_id and hasattr(email, 'mailing'):
        organization_election = email.mailing.organization_election
        source = email.mailing.source
        template = email.mailing.template
    else:
        organization_election = OrganizationElection.objects.select_related(
            'election',
            'election__state',
            'email_wrapper').get(
                election_id=election_id, organization=organization)

        if email:
            source = generate_source(email)
            template = email.mailingtemplate
        else:
            source = ''
            template = None


    election = organization_election.election
    state = election.state

    # Return the context
    return {
        'recipient': user,
        'organization': organization,
        'state': state,
        'email': email,
        'org_election': organization_election,
        'election': election,
        'source': source,
        'unsubscribe_url': unsubscribe_url,
        'manage_url': manage_url,
        'template': template
    }


@newrelic.agent.function_trace()
def render_template(source, context):
    """Render the final HTML of an email"""
    template_obj = Template(source)
    context_obj = Context(context)

    return template_obj.render(context_obj)


@newrelic.agent.function_trace()
def compose_block_preview(user_id, block_id, election_id, district_id=None):
    """Compose a preview of a block"""
    context = get_email_context(user_id, election_id=election_id)

    user = context['recipient']
    organization_election = context['org_election']
    wrapper = organization_election.email_wrapper

    block = Block.objects.get(pk=block_id)

    result = {
        'subject': u'{geodataset} {block}'.format(
            geodataset=block.geodataset.name, block=block.name),
        'from_name': user.organization.platform_name,
        'from_address': user.organization.from_address.address
    }

    districts = LegislativeDistrict.objects.filter(pk=district_id)

    block_context, block_source = compose_blocks(districts, block=block)

    final_email_source_components = []
    final_email_source_components.append(wrapper.header)
    final_email_source_components.append(block_source)
    final_email_source_components.append(wrapper.footer)

    final_email_source = '\n\n\n\n'.join(
        final_email_source_components)

    final_context = context.copy()
    final_context.update(block_context)

    result['body'] = html_link_sourcer(
        render_template(final_email_source, final_context),
        user, final_context['source'])

    return result


@newrelic.agent.function_trace()
def compose_pre_header(pre_header):
    """Compose the full HTML of the pre-header"""
    return mark_safe(u"""<span style="display:none !important;
        visibility:hidden; mso-hide:all; font-size:1px; color:#ffffff;
        line-height:1px; max-height:0px; max-width:0px; opacity:0;
        overflow:hidden;">{pre_header}</span>""".format(pre_header=pre_header))


@newrelic.agent.function_trace()
def compose_email(user_id, email_id, election_id, district_ids=None):
    """Compose an email

    Takes a bunch of context and returns a rendered HTML email.

    Args:
        user_id: the ID of a user account
        email_id: id of an Email object
        election_id: the id of an election
        district_ids: An list of district IDs to use for blocks (could also be
                      a `.values_list('id', flat=True)` queryset)
    """
    context = get_email_context(user_id, email_id=email_id,
                                election_id=election_id)

    email = context['email']

    if email.pre_header:
        pre_header = render_template(email.pre_header, context)
        context['pre_header'] = compose_pre_header(pre_header)
    else:
        pre_header = ''

    user = context['recipient']
    organization_election = context['org_election']
    wrapper = organization_election.email_wrapper

    rendered_from_name = render_template(email.from_name, context)

    from_address = formataddr(
        (rendered_from_name, user.organization.from_address.address))

    # We won't pass the context from the blocks into the subject and preheader
    # so to save complexity let's pass in the smaller context and render them
    # now
    result = {
        'subject': render_template(email.subject, context),
        'pre_header': pre_header,


        # We use these later on in the mailing process.

        'recipient_id': user.id,
        'from_address': from_address,
        'to_address': user.to_address,
        'organization_id': user.organization.id
    }

    if email:
        result['email_id'] = email.id
    else:
        result['email_id'] = None

    if district_ids is None:
        districts = user.location.districts.all()
    else:
        districts = LegislativeDistrict.objects.filter(id__in=district_ids)

    block_context, block_source = compose_blocks(districts, email=email)

    final_context = context.copy()
    final_context.update(block_context)

    final_email_source_components = []
    final_email_source_components.append(wrapper.header)
    final_email_source_components.append(email.body_above)
    final_email_source_components.append(block_source)
    final_email_source_components.append(email.body_below)
    final_email_source_components.append(wrapper.footer)

    final_email_source = '\n\n\n\n'.join(
        final_email_source_components)

    result['body'] = html_link_sourcer(
        render_template(final_email_source, final_context),
        user, final_context['source'])

    return result
