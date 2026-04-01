from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer,CategoryListSerializer ,ProductDetailSerializer,ProductListSerializer, ArticleSerializer

class MultipleSerializerMixin:
    detail_serializer_class = None
    
    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
class AdminArticleViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleViewset(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')
        if product_id is not None:
            queryset = queryset.filter(product_id = product_id)
        return queryset
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
# class ArticleViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):
#     serializer_class = ArticleListSerializer
#     detail_serializer_class = ArticleDetailSerializer
    
#     def get_queryset(self):
#         queryset = Article.objects.filter(active=True)
#         product_id = self.request.GET.get('product_id')
#         if product_id is not None:
#             queryset = queryset.filter(product_id = product_id)
#         return queryset
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return self.detail_serializer_class
#         return super().get_serializer_class()
    
#     @action(detail=True, methods=['post'])
#     def disable(self, request, pk):
#         self.get_object().disable()
#         return Response()
    
class ProductViewset(ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer
    
    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
        queryset = Product.objects.filter(active=True)
        # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id = category_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
# class ProductView(APIView):
    
#     def get(self, *args, **kwargs):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
    
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    queryset = Category.objects.all()

class CategoryViewset(MultipleSerializerMixin,ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
    
    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()
    
# class CategoryView(APIView):
    
#     def get(self, *args, **kwargs):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)