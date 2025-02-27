from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, Case, When, Value, FloatField
from django.db.models.functions import Cast
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal

from .serializers import ArticleSerializer, RatingSerializer, CategorySerializer, RatingSerializerNested
from .models import Article, Rating, Category
from .permissions import IsEditorOrReadOnly

class ArticleViewset(ModelViewSet):
    permission_classes = [IsEditorOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'cat_id' in self.request.GET:
            cat_id = int(self.request.GET['cat_id'])
            queryset = queryset.filter(category__id = cat_id)
        if 'editor_id' in self.request.GET:
            editor_id = int(self.request.GET['editor_id'])
            queryset = queryset.filter(editor = editor_id)
        if 'sort_by' in self.request.GET and self.request.GET['sort_by'] == 'rating':
            queryset = queryset.annotate(
                avg_rating = ExpressionWrapper(
                    Case(
                        When(rating_count=0, then=Value(-1)),
                        default=(Cast(F('total_rating'),FloatField()) / 
                                 Cast(F('rating_count'),FloatField())),
                        output_field=FloatField(),
                    ),
                    output_field=FloatField()
                )
            ).order_by('-avg_rating')
        if 'sort_by' in self.request.GET and self.request.GET['sort_by'] == 'time':
            queryset = queryset.order_by('-publishing_time')
        return queryset
    
class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class RateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class ArticleRatingsView(ListAPIView):
    serializer_class = RatingSerializerNested
    pagination_class = None
    queryset = Rating.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset() 
        if "article_id" in self.request.GET:
            article_id = int(self.request.GET["article_id"])
            queryset = queryset.filter(article__id = article_id)
        queryset = queryset.order_by("-time")
        return queryset