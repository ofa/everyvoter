"""Rendering Email Views"""
from django.http import JsonResponse, HttpResponse, Http404
from django.views.generic import View
from email_validator import validate_email, EmailNotValidError

from blocks.models import Block
from election.models import Election, LegislativeDistrict
from rendering.render_email import compose_email, compose_block_preview
from rendering.tasks import sample_email
from mailer.models import Email
from manage.mixins import ManageViewMixin


class EmailPreviewView(ManageViewMixin, View):
    """Generate HTML preview"""
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""

        email_id = request.GET.get('email', '')
        election_id = request.GET.get('election', '')
        ocd_ids = request.GET.get('ocd_ids', '').split(',')
        sample_address = request.GET.get('sample_address', '')

        if not email_id.isdigit() or not election_id.isdigit():
            raise Http404

        if not Email.objects.filter(
                id=email_id,
                organization=self.request.organization).exists():
            raise Http404

        if not Election.objects.filter(
                id=election_id).exists():
            raise Http404

        district_ids = LegislativeDistrict.objects.filter(
            ocd_id__in=ocd_ids).values_list('id', flat=True)

        result = compose_email(
            self.request.user.id,
            email_id,
            election_id,
            district_ids)

        if sample_address:
            # Try to verify sample address
            try:
                validated = validate_email(sample_address)
                email = validated['email']
                sample_email.apply_async(
                    kwargs={
                        'to_address': email,
                        'user_id': self.request.user.id,
                        'email_id': email_id,
                        'election_id': election_id,
                        'district_ids': list(district_ids)
                    },
                    priority=100
                )
                result['sample_result'] = 'Sample sent to {}'.format(email)
            except EmailNotValidError as error:
                result['sample_result'] = 'Sample Error: {}'.format(
                    unicode(error))

        if request.is_ajax():
            del result['organization_id']
            return JsonResponse(result)

        return HttpResponse(result['body'])


class BlockPreviewView(ManageViewMixin, View):
    """Generate preview of a block"""
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """Handle GET requests"""

        block_id = request.GET.get('block', '')
        election_id = request.GET.get('election', '')
        district_id = request.GET.get('district', '')

        if (not block_id.isdigit() or not election_id.isdigit() or not
                district_id.isdigit()):
            raise Http404

        if (not LegislativeDistrict.objects.filter(pk=district_id).exists() or
                not Election.objects.filter(pk=election_id).exists() or
                not Block.objects.filter(
                    id=block_id,
                    organization=self.request.organization,
                    geodataset__entry__district_id=district_id).exists()):
            raise Http404

        result = compose_block_preview(
            self.request.user.id, block_id, election_id, district_id)

        return HttpResponse(result['body'])
