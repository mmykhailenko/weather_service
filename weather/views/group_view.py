from django.contrib.auth.models import Group
from rest_framework import viewsets
from weather.serializers.group_serializer import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
