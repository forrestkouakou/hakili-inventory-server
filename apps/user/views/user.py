from rest_framework import viewsets

from apps.user.serializers import *


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-created_by')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserRoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be viewed or edited.
    """
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    # permission_classes = [permissions.IsAuthenticated]
