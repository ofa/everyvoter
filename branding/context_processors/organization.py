"""Organization Context Processor"""

def organization(request):
    """Context processor for organization"""
    return {'organization': request.organization}
