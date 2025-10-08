from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

# Import model and serializer from the local app structure
from .models import Leaves
from .serializers import LeavesSerializer

# Leaves List and Create View
class LeavesListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsAuthenticated()] # Require auth for both listing and creating
        return [IsAuthenticated()]
    
    def get(self, request):
        # By default, filter leaves to show only the current user's requests
        leaves = Leaves.objects.filter(is_deleted=False, user=request.user) 
        
        # If the user is staff, allow them to see ALL requests for review
        if request.user.is_staff:
            leaves = Leaves.objects.filter(is_deleted=False)
            
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Automatically set the user submitting the request
        data = request.data.copy()
        data['user'] = request.user.pk
        
        serializer = LeavesSerializer(data=data)
        if serializer.is_valid():
            # Automatically set created_by and updated_by to the current user
            serializer.save(created_by=request.user, updated_by=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Leaves Retrieve, Update, and Destroy View
class LeavesDetailView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            # Staff can access any leave request, standard user only their own
            if user.is_staff:
                 return Leaves.objects.get(pk=pk, is_deleted=False)
            else:
                 return Leaves.objects.get(pk=pk, user=user, is_deleted=False)
        except Leaves.DoesNotExist:
            return None
    
    def put(self, request, pk):
        leave = self.get_object(pk, request.user)
        if leave is None:
            return Response({'error': 'Leave not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeavesSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        leave = self.get_object(pk, request.user)
        if leave is None:
            return Response({'error': 'Leave not found or access denied'}, status=status.HTTP_404_NOT_FOUND)

        leave.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)
