from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Project 
from .serializers import ProjectSerializer 

class ProjectListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        projects = Project.objects.filter(is_deleted=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectDetailView(APIView): 
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            return None
    
    def get(self, request, pk):
        project = self.get_object(pk)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        project.is_deleted = True
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
Today's Work Update :-
User Management System with Django and PostgreSQL
- Update the code in a structured way
- Tested all API endpoints using Postman
- Fixed errors 

'''