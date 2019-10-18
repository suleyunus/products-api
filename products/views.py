from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .permissions import IsAdminOrReadOnly
from .models import Products
from .serializers import ProductSerializer
from .decorators import validate_request_data

class ProductsView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
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


class ProductDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        try:
            product = self.queryset.get(pk=kwargs["pk"])
            return Response(ProductSerializer(product).data)
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with ID: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data
    def put(self, request, *args, **kwargs):
        try:
            product = self.queryset.get(pk=kwargs["pk"])
            serializer = ProductSerializer()
            updated_product = serializer.update(product, request.data)
            return Response(ProductSerializer(updated_product).data)
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            product = self.queryset.get(pk=kwargs["pk"])
            product.delete()
            return Response(
                data={
                    "message": "Item deleted successfully"
                },
                status=status.HTTP_200_OK
            )
        except Products.DoesNotExist:
            return Response(
                data={
                    "message": "Product with ID: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )    
    