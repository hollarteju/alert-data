
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
from django.db.models import Count, OuterRef,Subquery
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

def timeline_logic():
        # user_pics = ProfilePicture.objects.get(user="olateju")
    num = Timeline.objects.count()
  
    react_value = Timeline.objects.order_by("-created_at").annotate(reaction = Count("reation__reaction", filter=models.Q(reation__reaction= "witness")),
                                   like = Count("reation__reaction", filter=models.Q(reation__reaction= "like")),
                                    dislike = Count("reation__reaction", filter=models.Q(reation__reaction= "dislike")),
                                    user_reaction = Subquery(Reaction.objects.filter(user =OuterRef("pk")).values("reaction")),
                                    
                        
                                    )
    
   
    lists = []
    for i in react_value:
        
        var = Timeline.objects.get(id = num)
        react = Reaction.objects.filter(user = var)
        reacter = [f"{i.username.username}-{i.reaction}"for i in react]
       
        num -=1
        try:
            pf_image = ProfilePicture.objects.get(user = i.user.id)
            data =  {   
                "user":i.user.username,
                "message":i.timeline_message,
                "media":i.timeline_media.name,
                "user_id":i.id,
                "profile_pic":pf_image.image.name,
                "witness":i.reaction,
                "like":i.like,
                "dislike":i.dislike,
                "user_reaction":i.user_reaction,
                "time":i.created_at,
                "reacter":reacter
                }
            lists.append(data)
        
        except ProfilePicture.DoesNotExist:
             data =  {   
                "user":i.user.username,
                "message":i.timeline_message,
                "media":i.timeline_media.name,
                "user_id":i.id,
                "witness":i.reaction,
                "like":i.like,
                "dislike":i.dislike,
                "user_reaction":i.user_reaction,
                "reacter":reacter
                }
             lists.append(data)
    
    return lists

@api_view(["POST"])
def timeline_message(request):
    data = request.data
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        timeline = Timeline.objects.get(id = data["id"])
        message = Message.objects.create(
                                        Messages = data["message"], 
                                         user = data["username"], 
                                         timeline_id = data["id"],
                                         message_media = data["media"]
                                         )
        message.timeline_instance.add(timeline)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def timeline_message_response(request):
    data = request.data
    serilizer = MessageSerializer(data= data)
    if serilizer.is_valid():
        timeline = Timeline.objects.get(id = data["id"])
        response = Message.objects.filter(timeline_instance = timeline)
        users_msg = [{"message":i.Messages, "user":i.user, "timeline_id":i.timeline_id} for i in response]
        empty_list =[]
        for i in response:
            try:
                username = UserData.objects.get(username = i.user)
                profile_pics = ProfilePicture.objects.get(user = username)
                users_msg = {
                            "message":i.Messages, 
                            "user":i.user, 
                            "timeline_id":i.timeline_id, 
                            "profile_pics":profile_pics.image.name,
                            "media": i.message_media.name
                             }
                empty_list.append(users_msg)
              
                
            except :
                users_msg = {
                            "message":i.Messages, 
                            "user":i.user, 
                            "timeline_id":i.timeline_id,
                            "media": i.message_media.name
                            }
            empty_list.append(users_msg)
        
        return Response(empty_list) 
        
        
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def timeline_response(request):
    result = timeline_logic()

    return Response(result)


@api_view(["POST"])
def user_reaction(request):
    users = Timeline.objects.annotate(name = models.F("reation__username__username"),
                                      user_active = models.F("reation__reaction"))
    list_values = [{"name":i.name, "user":i.user_active} for i in users]
    return Response(list_values) 

@api_view(["POST"])
def reaction_update(request):
    data = request.data
    serializer = ReactionSerializer(data = request.data)
    if serializer:
        username = UserData.objects.get(username = data["username"])
        try:
            user = Reaction.objects.get(user =data["id"],username = username)
            user.reaction = data["reaction"]
            user.save()
        except Reaction.DoesNotExist:
            timeline = Timeline.objects.get(id = data["id"])
            user = Reaction.objects.create(username =username,reaction = data["reaction"], user =timeline)
            user.save()
    
    result = timeline_logic()

    return Response(result)
# username: hollarteju1
# password hollarteju