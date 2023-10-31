
from django.shortcuts import render, get_list_or_404
from rest_framework  import viewsets, status
from . models import *
from . serializer import *
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# from urllib.parse import unquote

class MyTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        
    
        return token

class MyToken(TokenObtainPairView):
    serializer_class = MyTokenObtain

@api_view(["POST"])
def register_user(request):
    data = request.data
    serializer = UserDataSerializer(data=request.data)
    # password_validate(request.data)
    print(data)
    if serializer.is_valid():
        password_validate(data)
        print(email_validate(data))
        assert email_validate(data)
        user= UserData.objects.create_user(
                                            email = data["email"],
                                            username=data["username"],
                                            password=data["password"],

                                            )
      
        user.save()
            
        return Response(request.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["POST"])
def image_view(request):
    data = request.data
    
    try:
            user_data = UserData.objects.get(username =data["username"])
            user_data.username = data["user"]
            user_data.save()
            if ProfilePicture.objects.filter(user =user_data).exists():
                # ProfilePicture.objects.update(user= user_data,image = request.data["image"])
                user = ProfilePicture.objects.get(user =user_data)
                user.image = data["image"]
                user.avatar = data["avatar"]
                user.bio = data["bio"]
                user.save()
                return Response(data)
            else:
                user = ProfilePicture.objects.create(image = data["image"],
                                                      avatar = data["avatar"],
                                                      user =user_data,
                                                      bio= data["bio"])
                user.save()
                return Response(data)
    except UserData.DoesNotExist:
        return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    

@api_view(["POST"])
def profile_image_response(request):
        serializer = ProfilePictureSerializer(data= request.data)
        if serializer.is_valid():
            try:
                user = UserData.objects.get(username = request.data["username"])
                profile_image = ProfilePicture.objects.get(user=user)
                user_profile_image = {"image":profile_image.image.name,
                                      "avatar":profile_image.avatar.name,
                                      "bio": profile_image.bio}
                return Response(user_profile_image)
            except ProfilePicture.DoesNotExist:
                return Response(status=status.HTTP_200_OK)
                
                
  
        return Response(status= status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def timeline_update(request):
    data = request.data
    serializer= TimeLineSerializer(data=data)
    if serializer.is_valid():
        try:
            user = UserData.objects.get(username = data["username"])
            user_timeline = Timeline.objects.create(user = user, timeline_message = data["timeline_message"],
                                                     timeline_media= data["timeline_media"])
            user_timeline.save()
          
            return Response(status=status.HTTP_200_OK)
        except UserData.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def timeline_response(request):
    
        # user_pics = ProfilePicture.objects.get(user="olateju")
    react_value = Timeline.objects.order_by("-created_at").annotate(reaction = Count("reation__reaction", filter=models.Q(reation__reaction= "witness")),
                                   like = Count("reation__reaction", filter=models.Q(reation__reaction= "like")),
                                    dislike = Count("reation__reaction", filter=models.Q(reation__reaction= "dislike")),)
    
   
    lists = []  
    for i in react_value:
     
        try:
            pf_image = ProfilePicture.objects.get(user = i.user.id)
            a =  {   
                "user":i.user.username,
                "message":i.timeline_message,
                "media":i.timeline_media.name,
                "user_id":i.id,
                "profile_pic":pf_image.image.name,
                "witness":i.reaction,
                "like":i.like,
                "dislike":i.dislike
                }
            lists.append(a)
        except ProfilePicture.DoesNotExist:
             a =  {   
                "user":i.user.username,
                "message":i.timeline_message,
                "media":i.timeline_media.name,
                "user_id":i.id,
                "witness":i.reaction,
                "like":i.like,
                "dislike":i.dislike
                }
             lists.append(a)
    return Response(lists)

# username: hollarteju1
# password hollarteju


