from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated 
from .models import Task
from .serializers import TaskSerializer 

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assigned_to=user, is_deleted=False)

        if not tasks.exists():
            return Response(
                {'message': 'No tasks found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

       authenticated_user = request.user
       serializer = TaskSerializer(data=request.data)

       if serializer.is_valid():
           serializer.save(created_by=authenticated_user, updated_by=authenticated_user)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk, is_deleted=False)
        except Task.DoesNotExist:
            return None
    
    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.is_deleted = True
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)