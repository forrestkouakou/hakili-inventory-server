from rest_framework import viewsets, permissions

from apps.core import apps_config
from apps.product.models import (
    Brand,
    Category,
    Product,
)
from apps.product.serializers import (
    BrandSerializer,
    CategorySerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class BrandViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product brand to be viewed or edited.
    """
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Brand.objects.filter(company=self.kwargs['company_pk'])


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product category to be viewed or edited.
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(company=self.kwargs['company_pk'])


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product to be viewed or edited.
    """
    serializer_class = ProductReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(company=self.kwargs['company_pk'])

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in apps_config.WRITE_METHODS:
            serializer_class = ProductWriteSerializer

        return serializer_class
