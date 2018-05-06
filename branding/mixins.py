"""Branding-related Mixins"""
from django.db import models


class OrganizationMixin(models.Model):
    """Model that has a specific branding"""
    organization = models.ForeignKey(
        'branding.Organization', editable=False, db_index=True)

    class Meta(object):
        """Meta options for abstract model"""
        abstract = True


class OrganizationManagerMixin(object):
    """Mixin for model managers"""
    def for_user(self, user):
        """Generator for a specific user"""
        if user.is_superuser:
            return self.get_queryset()

        return self.get_queryset().filter(organization=user.organization)


class OrganizationViewMixin(object):
    """View for filtering by organization"""
    def get_queryset(self):
        """Get the queryset filtered by organization"""
        queryset = super(OrganizationViewMixin, self).get_queryset()
        return queryset.filter(organization=self.request.organization)


class OrganizationCreateViewMixin(object):
    """Assign an organization to an object in a CreateView"""
    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.organization = self.request.organization

        return super(OrganizationCreateViewMixin, self).form_valid(form)
