from rest_framework import viewsets, permissions

from apps.company.serializers import *
from apps.core import apps_config


class CompanyTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = CompanyType.objects.all()
    serializer_class = CompanyTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompanyPermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = CompanyPermission.objects.all().order_by('id')
    serializer_class = CompanyPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows all roles to be viewed or edited.
    """
    queryset = CompanyRole.objects.all().order_by('id')
    serializer_class = CompanyRoleReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = CompanyRoleWriteSerializer

        return serializer_class


class CompanyRoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows a company roles to be viewed or edited.
    """
    serializer_class = CompanyRoleReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CompanyRole.objects.filter(companies__id=self.kwargs['company_pk'])

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = CompanyRoleWriteSerializer

        return serializer_class


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    # queryset = Company.objects.company_list().prefetch_related("roles")
    queryset = Company.objects.company_list()
    serializer_class = CompanyReadSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = CompanyWriteSerializer

        return serializer_class


class CompanyDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = CompanyDetails.objects.all()
    serializer_class = CompanyDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
