from django.contrib.auth import get_user_model
from rest_framework import serializers
# from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        print("in create userserializer")
        try:
            user = get_user_model().objects.create(
                username=validated_data['username'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception:
            return None

    class Meta:
        model = get_user_model()
        fields = ('username','email', 'password','created_at', 'updated_at', 'first_name', 'last_name', 'pk')
