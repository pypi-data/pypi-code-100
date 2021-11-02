from django.contrib.auth import get_user_model

from .models import FrontData, FAQ

try:
    from rest_framework import serializers

    User = get_user_model()


    class FrontDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = FrontData
            fields = ('name', 'data')


    class StdFrontDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = FrontData
            fields = ('name', 'data', 'templates', 'created_at')


    class FullFrontDataSerializer(serializers.ModelSerializer):
        class Meta:
            model = FrontData
            fields = '__all__'

        def validate(self, attrs):
            if isinstance(self.context['request'].user, User):
                attrs['user'] = self.context['request'].user
            return attrs


    class FAQSerializer(serializers.ModelSerializer):
        class Meta:
            model = FAQ
            fields = '__all__'
except (ModuleNotFoundError, ImportError):
    class FrontDataSerializer:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class StdFrontDataSerializer:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class FullFrontDataSerializer:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class FAQSerializer:
        """Don't use this. Install djangorestframework before using this"""
        pass


    print("****djangorestframework is not installed. Some feature won't work. module: front_data****")
