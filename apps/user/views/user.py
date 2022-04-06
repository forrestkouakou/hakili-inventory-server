from rest_framework import viewsets, permissions

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
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_model().people.user_list().filter(company=self.kwargs['company_pk'])
