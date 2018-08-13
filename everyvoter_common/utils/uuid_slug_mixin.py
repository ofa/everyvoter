"""Handle views that use UUIDs as slugs"""
from django.http import Http404


class UUIDSlugMixin(object):
    """Mixin for views that rely on UUIDs"""
    def get_object(self, *args, **kwargs):
        """Get the object, handle common bad-UUID exceptions"""
        try:
            django_object = super(UUIDSlugMixin, self).get_object(
                *args, **kwargs)
        except ValueError as value_error:
            if (unicode(value_error.message) ==
                    u'bytes is not a 16-char string'):
                raise Http404
            raise
        except TypeError as type_error:
            if unicode(type_error.message) == u'Incorrect padding':
                raise Http404
            raise

        return django_object
