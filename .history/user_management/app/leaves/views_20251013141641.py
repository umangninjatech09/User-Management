from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Leaves
from .serializers import LeavesSerializer

# Leaves Views

class LeavesListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        leaves = Leaves.objects.filter(created_by=user, is_deleted=False)

        if not leaves.exists():
            return Response(
                {'message': 'No leaves found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        authenticated_user = request.user
        serializer = LeavesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=authenticated_user, created_by=authenticated_user, updated_by=authenticated_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        if leave.user != request.user:
            return Response(
                {'error': 'You do not have permission to update this leave request.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Handle the update process
        # Note: We must restrict which fields the user can update (e.g., they cannot change 'approved_status')
        serializer = LeavesSerializer(leave, data=request.data)
        if serializer.is_valid():
            # Update the audit field
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# --------------------------------------------------------------------------------

    def delete(self, request, pk):
        try:
            # 1. Retrieve the active leave object
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. **PERMISSION CHECK: Only the owner can delete (soft-delete) the leave**
        if leave.user != request.user:
            return Response(
                {'error': 'You do not have permission to delete this leave request.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        # 3. Soft-delete the object (using your model's custom delete method or logic)
        leave.is_deleted = True
        
        # Optionally, you can set the updated_by field here too for the audit trail
        # leave.updated_by = request.user 
        
        leave.save()
        return Response(status=status.HTTP_204_NO_CONTENT)