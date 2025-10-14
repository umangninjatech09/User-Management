from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated 
# Assuming Task model and TaskSerializer are imported or defined in the same way as Project
from .models import Task
from .serializers import TaskSerializer 

class TaskListCreateView(APIView):
    """
    Handles listing all active Tasks (GET) and creating a new Task (POST).
    GET is allowed for any user (AllowAny).
    POST requires an authenticated user (IsAuthenticated).
    """

    # Custom permission logic based on the request method
    def get_permissions(self):
        if self.request.method == 'GET':
            # Allow anyone to view the list of active tasks
            return [AllowAny()]
        # Require authentication for creating a new task (POST)
        return [IsAuthenticated()]

    def get(self, request):
        # Filter for active tasks only (is_deleted=False)
        tasks = Task.objects.filter(is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Authentication is handled by get_permissions()
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Soft deletion field is typically set to False by default on model, 
            # so we just save the task.
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------

class TaskDetailView(APIView):
    """
    Handles retrieving (GET), updating (PUT), and soft-deleting (DELETE) a specific Task.
    All operations require an authenticated user (IsAuthenticated).
    """
    # Set the default permission for GET, PUT, and DELETE methods
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            # Only retrieve tasks that are NOT soft-deleted
            return Task.objects.get(pk=pk, is_deleted=False)
        except Task.DoesNotExist:
            return None
    
    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            # Consistent error response for not found
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            # Consistent error response for not found
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            # Consistent error response for not found
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        # Apply soft deletion instead of permanent deletion
        task.is_deleted = True
        task.save()
        # 204 No Content for successful deletion (soft-delete)
        return Response(status=status.HTTP_204_NO_CONTENT)