from rest_framework import serializers
from . models import *
from django.contrib.auth import authenticate

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = "__all__"
    

class UserDataLoginSerializer(serializers.Serializer):    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def authenticating(data_recieved):
        
        user =authenticate(username=data_recieved["username"], password=data_recieved["password"])
        if not user:
            raise AttributeError("wrong input")
        else:
            return user
        
class ProfilePictureSerializer(serializers.Serializer):
    # image = serializers.ImageField()
    class Meta:
        model=ProfilePicture
        fields = "__all__"

            
class TimeLineSerializer(serializers.Serializer):
    class Meta:
        model=Timeline
        fields = "__all__"

class MessageSerializer(serializers.Serializer):
    class Meta:
        model=Message
        fields = "__all__"


class ReactionSerializer(serializers.Serializer):
    class Meta:
        model=Reaction
        fields = "__all__"

    # def create(self, validated_data):
    #     user = self.context["request"].data["user"]
    #     verify_user = self.get_user(user)

    #     image = ImageData.objects.create(
    #         user=verify_user,
    #         image = validated_data.get["image"]
    #     )
    #     image.save()
    #     return image
    

    def get_user(self, user_id):
        try:
            user = UserData.objects.get(id=user_id)
        except UserData.DoesNotExist:
            raise serializers.ValidationError("User Does Not Exist")
        return user
    
