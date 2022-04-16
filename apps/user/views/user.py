from rest_framework import viewsets, permissions

from apps.core import apps_config
from apps.user.serializers import *


class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user permissions to be viewed or edited.
    """
    queryset = UserPermission.objects.all().order_by('id')
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    # TODO: Verify that superusers can not be logged into the mobile app
    #   Check inside the USER_AGENT
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_model().people.user_list().filter(company=self.kwargs['company_pk'])

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = UserSerializer

        return serializer_class


class InstallationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows installation to be viewed or edited.
    """
    queryset = Installation.objects.all().order_by('datetime')
    serializer_class = InstallationSerializer
    permission_classes = [permissions.IsAuthenticated]
