"""Views for blocks"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView, UpdateView, ListView, FormView, DetailView, DeleteView
)
from django.views.generic.detail import BaseDetailView
from django.urls import reverse_lazy, reverse
from django_filters.views import FilterView

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from blocks.models import Block, BlockCategory
from blocks.forms import BlockModelForm, BlockPreviewForm
from blocks.filters import BlockFilter
from everyvoter_common.utils.soft_delete import SoftDeleteView


class BlockListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all blocks"""
    queryset = Block.objects.select_related(
        'geodataset', 'organization').order_by('pk')
    model = Block
    paginate_by = 10
    context_object_name = 'blocks'
    filterset_class = BlockFilter
    template_name_suffix = '_list'

    def get_context_data(self, *args, **kwargs):
        """Get the context for the page"""
        response = super(BlockListView, self).get_context_data(*args, **kwargs)

        # Only allow filtering of categories contained in its own organization
        response['filter'].filters['categories'].queryset = response[
            'filter'].filters['categories'].queryset.filter(
                organization=self.request.organization)

        return response


class BlockCreateModifyObjectViewMixin(object):
    """Mixin for views that crea modify blocks"""
    def get_form(self):
        """Get the form, but with categories scoped to that user's org"""
        form = super(BlockCreateModifyObjectViewMixin, self).get_form()
        form.fields['categories'].queryset = form.fields['categories'].queryset.filter(
            organization=self.request.organization)
        form.fields['geodataset'].queryset = form.fields['geodataset'].queryset.filter(
            organization=self.request.organization)
        return form

    def get_success_url(self):
        """Get the success URL"""
        if 'save_preview' in self.request.POST:
            return reverse(
                'manage:blocks:preview_block', args=[self.object.uuid])
        return super(BlockCreateModifyObjectViewMixin, self).get_success_url()


class BlockCreateView(ManageViewMixin, SuccessMessageMixin,
                      OrganizationCreateViewMixin,
                      BlockCreateModifyObjectViewMixin, CreateView):
    """Create a block"""
    model = Block
    form_class = BlockModelForm
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was created"


class BlockUpdateView(ManageViewMixin, SuccessMessageMixin,
                      BlockCreateModifyObjectViewMixin, OrganizationViewMixin,
                      UpdateView):
    """Edit a block"""
    model = Block
    slug_field = 'uuid'
    form_class = BlockModelForm
    context_object_name = 'content_block'
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was edited"


class BlockPreviewView(ManageViewMixin, OrganizationViewMixin, BaseDetailView,
                       FormView):
    """Preview a block"""
    model = Block
    slug_field = 'uuid'
    form_class = BlockPreviewForm
    template_name = 'blocks/block_preview.html'
    context_object_name = 'content_block'

    def get_form(self):
        """Get the form"""
        form = super(BlockPreviewView, self).get_form()
        form.fields['district'].queryset = form.fields['district'].queryset.filter(
            entry__geodataset__block=self.object)
        form.fields['block'].initial = self.object.id
        return form



class BlockDeleteView(ManageViewMixin, SuccessMessageMixin,
                      OrganizationViewMixin, SoftDeleteView):
    """Delete a block"""
    model = Block
    slug_field = 'uuid'
    context_object_name = 'content_block'
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was deleted"


class BlockCategoryListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all block tags"""
    model = BlockCategory
    paginate_by = 10
    context_object_name = 'blockcategories'


class BlockCategoryCreateView(ManageViewMixin, SuccessMessageMixin,
                              OrganizationCreateViewMixin, CreateView):
    """Create a block category"""
    model = BlockCategory
    fields = ['name']
    success_url = reverse_lazy('manage:blocks:list_blockcategories')
    success_message = "Block Category %(name)s was created"


class BlockCategoryUpdateView(ManageViewMixin, SuccessMessageMixin,
                              OrganizationViewMixin, UpdateView):
    """Edit a block category"""
    model = BlockCategory
    slug_field = 'uuid'
    fields = ['name']
    context_object_name = 'blockcategory'
    success_url = reverse_lazy('manage:blocks:list_blockcategories')
    success_message = "Block Category %(name)s was edited"


class BlockCategoryDeleteView(ManageViewMixin, SuccessMessageMixin,
                              OrganizationViewMixin, DeleteView):
    """Delete a block category"""
    model = BlockCategory
    slug_field = 'uuid'
    context_object_name = 'blockcategory'
    success_url = reverse_lazy('manage:blocks:list_blockcategories')
    success_message = "Block Category %(name)s was deleted"
