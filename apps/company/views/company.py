from rest_framework import viewsets

from apps.company.serializers import *


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer
    # permission_classes = [permissions.IsAuthenticated]


class CompanyTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    # permission_classes = [permissions.IsAuthenticated]
