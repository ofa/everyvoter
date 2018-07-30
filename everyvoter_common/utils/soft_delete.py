"""Functionality that allows soft deletion"""
from django.db import models
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView


class SoftDeleteModel(models.Model):
    """Abstract model that allows soft-deletion"""
    deleted = models.BooleanField(
        'Deleted', db_index=True, editable=False, default=False)

    class Meta(object):
        """Meta info for soft-deletable mixin"""
        abstract = True


class SoftDeleteView(DeleteView):
    """DeleteView without actual deletion"""
    def delete(self, request, *args, **kwargs):
        """Soft delete the object"""
        # pylint: disable=attribute-defined-outside-init
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.deleted = True
        self.object.save()

        return HttpResponseRedirect(success_url)


class ActiveManager(models.Manager):
    """Only show models that exist"""
    def get_queryset(self):
        """Get the queryset removing all deleted objects"""
        return super(ActiveManager, self).get_queryset().filter(deleted=False)
