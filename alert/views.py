
from django.shortcuts import render
from rest_framework  import viewsets, status
from . models import *
from . serializer import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView
from urllib.parse import unquote

class MyTokenObtain(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["phone_number"] = user.phone_number
        token["state"] = user.state
        token["city"] = user.city
        token["district"] = user.district
        
    
        return token

class MyToken(TokenObtainPairView):
    serializer_class = MyTokenObtain

@api_view(["POST"])
def register_user(request):
   
    serializer = UserDataSerializer(data=request.data)
    # password_validate(request.data)
    if serializer.is_valid():
        user= UserData.objects.create_user(username=request.data["username"], password=request.data["password"])
      
        user.save()
            
        return Response(request.data)
   
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# # @api_view(["POST"])
# # def login_page(request):
# #     data = request.data
    
# #     serializer = UserDataLoginSerializer(data=data)
# #     if serializer.is_valid():
        
# #         user= UserDataLoginSerializer.authenticating(data)
# #         login(request, user)

# #         user_datas = request.user
# #         user_data = {
# #             "username": user_datas.username,
# #             "phone_number": user_datas.phone_number,
# #             "state": user_datas.state,
# #             "city": user_datas.city,
# #             "district":user_datas.district
# #             }
# #         return Response(user_data)
        
  
# #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def logout_users(request):
#     logout(request)
#     return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def image_view(request):
    
    serializer = ProfilePictureSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user_data = UserData.objects.get(username = request.data["username"])
            user_data.username = request.data["username"]
            
            user_data.save()
            if ProfilePicture.objects.filter(user = user_data).exists():
                # ProfilePicture.objects.update(user= user_data,image = request.data["image"])
                user = ProfilePicture.objects.get(user = user_data)
                user.image = request.data["image"]
                user.avatar = request.data["avatar"]
                user.save()
                return Response(request.data)
            else:
                user = ProfilePicture.objects.create(image = request.data["image"], avatar = request.data["avatar"] ,user =user_data)
                user.save()
                return Response(request.data)
        except UserData.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
def profile_image_response(request):
        serializer = ProfilePictureSerializer(data= request.data)
        if serializer.is_valid():
            try:
                user = UserData.objects.get(username = request.data["username"])
                profile_image = ProfilePicture.objects.get(user=user)
                user_profile_image = {"image":profile_image.image.name,
                                      "avatar":profile_image.avatar.name}
                return JsonResponse(user_profile_image)
            except ProfilePicture.DoesNotExist:
                return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                
                
  
        return Response(status= status.HTTP_401_UNAUTHORIZED)
# class ImageView(ListCreateAPIView):
#     queryset = ImageData.objects.all()
#     serializer_class=ImageSerializer()

