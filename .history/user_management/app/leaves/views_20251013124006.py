from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Leaves
from .serializers import LeavesSerializer

# Leaves Views

class LeavesListCreateView(APIView):
    peri
    
    def get(self, request):
        leaves = Leaves.objects.filter(is_deleted=False)
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LeavesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeavesSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        leave.is_deleted = True
        leave.save()
        return Response(status=status.HTTP_204_NO_CONTENT)