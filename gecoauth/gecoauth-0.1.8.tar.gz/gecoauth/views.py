from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status

from .serializers import GecoRegisterSerializer
from .models import GecoUser
# Create your views here.

class GecoRegisterView(RegisterView):

    serializer_class = GecoRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        
        geco_user = GecoUser.objects.get(user=user)
        project_dir = geco_user.project_dir

        headers = self.get_success_headers(serializer.data)

        response = self.get_response_data(user)
        response['project_dir'] = project_dir
        return Response(response,
                        status=status.HTTP_201_CREATED,
                        headers=headers)