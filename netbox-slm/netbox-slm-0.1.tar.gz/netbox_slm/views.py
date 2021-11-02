from django.shortcuts import render
from django.views.generic import View


class SoftwareLifecycleManagementView(View):
    def get(self, request):
        return render(request, 'netbox_slm/index.html', {
            'msg': 'hello',
        })