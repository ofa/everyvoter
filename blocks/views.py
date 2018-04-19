"""Views for blocks"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django_filters.views import FilterView

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin, OrganizationCreateViewMixin
from blocks.models import Block, BlockTag
from blocks.filters import BlockFilter


class BlockListView(OrganizationViewMixin, ManageViewMixin, FilterView):
    """List all blocks"""
    model = Block
    queryset = Block.objects.select_related('tag')
    paginate_by = 10
    context_object_name = 'blocks'
    filterset_class = BlockFilter
    template_name_suffix = '_list'


class BlockCreateView(ManageViewMixin, SuccessMessageMixin,
                      OrganizationCreateViewMixin, CreateView):
    """Create a block"""
    model = Block
    template_name_suffix = '_create'
    fields = ['name', 'tag', 'code']
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was created"


class BlockUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Edit a block"""
    model = Block
    slug_field = 'uuid'
    template_name_suffix = '_edit'
    fields = ['name', 'tag', 'code']
    context_object_name = 'content_block'
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was edited"


class BlockDeleteView(ManageViewMixin, SuccessMessageMixin, DeleteView):
    """Delete a block"""
    model = Block
    slug_field = 'uuid'
    context_object_name = 'content_block'
    success_url = reverse_lazy('manage:blocks:list_blocktags')
    success_message = "Block %(name)s was deleted"


class BlockTagListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all block tags"""
    model = BlockTag
    paginate_by = 10
    context_object_name = 'blocktags'


class BlockTagCreateView(ManageViewMixin, SuccessMessageMixin,
                         OrganizationCreateViewMixin, CreateView):
    """Create a block tag"""
    model = BlockTag
    template_name_suffix = '_create'
    fields = ['name']
    success_url = reverse_lazy('manage:blocks:list_blocktags')
    success_message = "Block Tag %(name)s was created"


class BlockTagUpdateView(ManageViewMixin, SuccessMessageMixin, UpdateView):
    """Edit a block tag"""
    model = BlockTag
    slug_field = 'uuid'
    template_name_suffix = '_edit'
    fields = ['name']
    context_object_name = 'blocktag'
    success_url = reverse_lazy('manage:blocks:list_blocktags')
    success_message = "Block Tag %(name)s was edited"


class BlockTagDeleteView(ManageViewMixin, SuccessMessageMixin, DeleteView):
    """Delete a block tag"""
    model = BlockTag
    slug_field = 'uuid'
    context_object_name = 'blocktag'
    success_url = reverse_lazy('manage:blocks:list_blocktags')
    success_message = "Block Tag %(name)s was deleted"
