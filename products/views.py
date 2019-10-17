from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductSerializer

class ProductsView(APIView):
    def get(self, request, format=None):
        all_products = Products.objects.all()
        serializers = ProductSerializer(all_products, many=True)
        return Response(serializers.data)
