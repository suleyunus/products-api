from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .permissions import isAdminOrReadOnly
from .models import Products
from .serializers import ProductSerializer

class ProductsView(APIView):
    permission_classes = (isAdminOrReadOnly,)
    def get(self, request, format=None):
        all_products = Products.objects.all()
        serializers = ProductSerializer(all_products, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProductSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
