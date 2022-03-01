from rest_framework import viewsets

from apps.company.serializers import *


class CompanyTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CompanyRoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company roles to be viewed or edited.
    """
    queryset = CompanyRole.objects.all().order_by('id')
    serializer_class = CompanyRoleSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = Company.objects.company_list()
    serializer_class = CompanySerializer
    # permission_classes = [permissions.IsAuthenticated]


class CompanyDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanyDetailsSerializer
    # permission_classes = [permissions.IsAuthenticated]
