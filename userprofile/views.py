from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class SetRoleAsEditor(APIView):
    permission_classes = [IsAuthenticated,]
    
    def post(self, request):
        try:
            user = request.user
            user.userprofile.role = "editor"
            user.userprofile.save()
            return Response({
                "message": "Success"
            })
        except Exception as e:
            return Response({
                "error": repr(e)
            })
        
class GetRoleView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        try:
            user = request.user
            return Response({
                "role": user.userprofile.role
            })
        except Exception as e:
            return Response({
                "error": repr(e)
            })
