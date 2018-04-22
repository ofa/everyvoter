"""Organization Context Processor"""

def organization(request):
    """Context processor for organization"""
    if hasattr(request, 'organization'):
        return {'organization': request.organization}
    else:
        return {'organization': None}
