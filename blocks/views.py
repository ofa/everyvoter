"""Views for blocks"""
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy

from manage.mixins import ManageViewMixin
from branding.mixins import OrganizationViewMixin
from blocks.models import Block, BlockTag


class BlockListView(OrganizationViewMixin, ManageViewMixin, ListView):
    """List all blocks"""
    model = Block
    paginate_by = 10
    context_object_name = 'blocks'


class BlockCreateView(ManageViewMixin, SuccessMessageMixin, CreateView):
    """Create a block"""
    model = Block
    template_name_suffix = '_create'
    fields = ['name', 'tag', 'code']
    success_url = reverse_lazy('manage:blocks:list_blocks')
    success_message = "Block %(name)s was created"

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.organization = self.request.organization

        return super(BlockCreateView, self).form_valid(form)


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


class BlockTagCreateView(ManageViewMixin, SuccessMessageMixin, CreateView):
    """Create a block tag"""
    model = BlockTag
    template_name_suffix = '_create'
    fields = ['name']
    success_url = reverse_lazy('manage:blocks:list_blocktags')
    success_message = "Block Tag %(name)s was created"

    def form_valid(self, form):
        """Handle a valid form"""
        form.instance.organization = self.request.organization

        return super(BlockTagCreateView, self).form_valid(form)


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
