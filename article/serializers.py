from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Article, Rating, Category

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'headline', 'body', 'publishing_time', 'avg_rating', 'editor', 'category', 'image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'article', 'value', 'time', 'body']

class RatingSerializerNested(RatingSerializer):
    user = UserSerializer(read_only=True)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'