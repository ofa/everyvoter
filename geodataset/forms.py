"""Forms for account app"""
from django import forms

from geodataset.models import GeoDataset
from geodataset.validators import validate_geodataset_upload


class GeoDatasetUploadForm(forms.ModelForm):
    """Upload a geodataset"""
    file = forms.FileField(validators=[validate_geodataset_upload])

    class Meta(object):
        """Meta options for form"""
        model = GeoDataset
        fields = ['name', 'categories', 'file']
