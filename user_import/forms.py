"""Forms for user import"""
import unicodecsv

from django import forms
from django.core.exceptions import ValidationError

from user_import.models import UserImport



class UserImportForm(forms.ModelForm):
    """Form for creating/starting a new import"""

    def clean_file(self):
        """Clean the file field"""
        the_file = self.cleaned_data['file']

        # Confirm the file has the correct headers. Because we're using
        # exclusively `TemporaryFileUploadHandler`s we'll always have a local
        # file we can open and inspect for the field names.
        with open(the_file.temporary_file_path(), 'rb') as file_obj:
            reader = unicodecsv.DictReader(file_obj, encoding='utf-8-sig')
            if reader.fieldnames != [u'first_name',
                                     u'last_name',
                                     u'email',
                                     u'address']:
                raise ValidationError('Invalid Fieldnames. Use the template.')

        return the_file

    class Meta(object):
        """Meta options for the form"""
        model = UserImport
        fields = ['name', 'file']
