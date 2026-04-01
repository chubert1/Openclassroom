from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
from shop.models import Category, Product, Article


# class ArticleListSerializer(ModelSerializer):
#     class Meta:
#         model = Article
#         fields= ['id', 'date_created', 'date_updated', 'name', 'price']
#     def validate_price(self, value):
#         if value < 1:
#             raise ValidationError('Le prix doit être supérieur a 1')
#         return value
#     def validate_product(self, value):
#         if value.active is False:
#             raise ValidationError('Produit inactif')
#         return value

class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields= ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
        
    def validate_price(self, value):
        if value < 1:
            raise ValidationError('Le prix doit être supérieur a 1')
        return value
    def validate_product(self, value):
        if value.active is False:
            raise ValidationError('Produit inactif')
        return value
    
# class ArticleDetailSerializer(ModelSerializer):
#     class Meta:
#         model = Article
#         fields= ['id', 'date_created', 'date_updated', 'name', 'price', 'product']
        
#     def get_prroduct(self, instance):
#         queryset = instance.product.filter(active=True)
#         serializer = ProductListSerializer(queryset, many=True)
#         return serializer.data
#     def validate_price(self, value):
#         if value < 1:
#             raise ValidationError('Le prix doit être supérieur a 1')
#         return value
#     def validate_product(self, value):
#         if value.active is False:
#             raise ValidationError('Produit inactif')
#         return value
    
class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category','ecoscore']
        
class ProductDetailSerializer(ModelSerializer):
    articles = SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']
        
    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data
    
    
        

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description']   
        
    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise ValidationError('Une catégorie avec ce nom existe déjà.')  
        return value
    
    def validate(self, data):
        if data['name'] not in data['description']:
            raise ValidationError('Le nom de la catégorie doit être dans la description')
        return data
    
class CategoryDetailSerializer(ModelSerializer):
    products = SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'products']
        
    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductListSerializer(queryset, many=True) 
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data     