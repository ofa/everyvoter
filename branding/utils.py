"""Utilities for brandings"""
from django.template import loader as template_loader


def org_domain_cache_key(domain):
    """Cache key for an organization by domain"""
    return u'org' + domain


# pylint: disable=invalid-name, too-many-arguments
def get_or_create_organization(name, platform_name, hostname, homepage,
                               organization_model=None,
                               domain_model=None,
                               emailwrapper_model=None):
    """Get or create a a new organization

    Creates a new organization on the platform. Designed to be used during
    initial migrations, in tests, and in production, this task sets up an
    organization to be in a state ready to have users added. As new features
    are added to the app that are necessary for all organizations to have, it
    should be added to this method.

    If the domain already exists, returns the attached organization.

    Args:
        name: Name of the organization
        platform_name: Name the organization is using for EveryVoter
        hostname: hostname the platform will be initially hosted on
        homepage: homepage of the organization
        organization_model: optional Organization model (so migrations can pass
                            in models in the state they exist inside that
                            migration) (default: {None})
        domain_model: optional Domain model (for migrations) (default: {None})
        emailwrapper_model: EmailWrapper model (for migrations)
                            (default: {None})

    Returns:
        new/existing organization, created true/false
        tuple (organization, boolean)
    """

    # Since this could be used in a migration, we need to be able to pass in
    # the models themselves as they exist in that migration.
    if not organization_model or not domain_model:
        from branding.models import (
            Organization, Domain
        )
    else:
        Organization = organization_model
        Domain = domain_model

    if not emailwrapper_model:
        from mailer.models import EmailWrapper
    else:
        EmailWrapper = emailwrapper_model

    try:
        domain = Domain.objects.get(hostname=hostname)
        return domain.organization, False
    except Domain.DoesNotExist:
        pass


    new_organization = Organization(
        name=name,
        platform_name=platform_name,
        homepage=homepage,
        privacy_url='',
        terms_url=''
    )

    new_organization.save()

    new_domain = Domain(
        organization=new_organization, hostname=hostname).save()

    new_organization.primary_domain = new_domain
    new_organization.save()

    wrapper = EmailWrapper(
        organization=new_organization,
        name='Default',
        default=True
    )


    header_path = template_loader.get_template(
        'mailer/wrappers/default_header.html').origin.name
    with open(header_path, 'r') as header_file:
        wrapper.header = header_file.read()

    footer_path = template_loader.get_template(
        'mailer/wrappers/default_footer.html').origin.name
    with open(footer_path, 'r') as footer_file:
        wrapper.footer = footer_file.read()

    wrapper.save()

    return new_organization, True
