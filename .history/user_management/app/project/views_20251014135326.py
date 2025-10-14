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
        authenticated_user = request.user
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            project_instance = serializer.save(created_by=authenticated_user, updated_by=authenticated_user)

            if authenticated_user not in project_instance.users.all():
                    project_instance.users.add(authenticated_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView): 
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            return None

    def get(self, request):
        user = request.user 
        projects = Project.objects.filter(users=user, is_deleted=False)

        if not projects.exists():
            return Response(
                {'message': 'No projects found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object(pk)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in project.users.all():
            return Response(
                {'error': 'You do not have permission to update this project.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProjectSerializer(project, data=request.data, )
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        project = self.get_object(pk)
        if project is None:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in project.users.all():
            return Response(
                {'error': 'You do not have permission to delete this project.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        project.is_deleted = True
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
