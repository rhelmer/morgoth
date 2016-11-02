import json

from rest_framework import permissions, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from morgoth.addons.api.serializers import AddonSerializer, AddonGroupSerializer
from morgoth.addons.models import Addon, AddonGroup
from morgoth.base.utils import BalrogAPI


class AddonViewSet(ModelViewSet):
    queryset = Addon.objects.all()
    serializer_class = AddonSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]

    @detail_route(methods=['GET'])
    def groups(self, request, *args, **kwargs):
        addon = self.get_object()
        serializer = AddonGroupSerializer(addon.groups.all(), many=True)
        return Response(serializer.data)


class AddonGroupViewSet(ModelViewSet):
    queryset = AddonGroup.objects.all()
    serializer_class = AddonGroupSerializer
    permission_classes = [
        permissions.DjangoModelPermissionsOrAnonReadOnly,
    ]

    @list_route(methods=['POST'])
    def update_built_in(self, request, *args, **kwargs):
        browser_version = request.data.get('browser_version')
        if not browser_version:
            return Response({'browser_version': 'A browser version is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        group, _ = AddonGroup.objects.get_or_create(browser_version=browser_version)

        addons = request.data.get('addons')
        if not isinstance(addons, list):
            return Response({'addons': 'A list of addon IDs is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        group.built_in_addons.clear()

        for addon in request.data.get('addons'):
            addon, _ = Addon.objects.get_or_create(name=addon.get('name'),
                                                   version=addon.get('version'))
            group.built_in_addons.add(addon)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'])
    def add_addons(self, request, *args, **kwargs):
        group = self.get_object()
        addon_ids = request.data.get('addon_ids', [])
        addons = Addon.objects.filter(id__in=addon_ids)

        if len(addon_ids) != addons.count():
            return Response({'addon_ids': 'One or more of the IDs provided were invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        for addon in addons:
            group.addons.add(addon)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'])
    def remove_addons(self, request, *args, **kwargs):
        group = self.get_object()
        addon_ids = request.data.get('addon_ids', [])
        addons = Addon.objects.filter(id__in=addon_ids)

        for addon in addons:
            group.addons.remove(addon)

        if len(addon_ids) != addons.count():
            return Response({'addon_ids': 'One or more of the IDs provided were invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['POST'])
    def sync(self, request, *args, **kwargs):
        group = self.get_object()
        balrog = BalrogAPI(auth=request.ldap)

        balrog.request('releases', method='POST', data={
            'name': group.name, 'product': 'SystemAddons', 'blob': json.dumps(group.release_data)})

        balrog.request('rules', method='POST', data={
            'priority': 1000, 'backgroundRate': 100, 'product': 'SystemAddons',
            'version': group.browser_version, 'mapping': group.name,
            'comment': 'Generated by Morgoth.'})

        return Response(status=status.HTTP_204_NO_CONTENT)
