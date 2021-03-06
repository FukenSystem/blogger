from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User
from blog import models
from . import serializers
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    this viewset provides 'list' and 'retrieve' actions to everyone.
    'create', 'update' and 'destroy' actions to admins only.
    The 'list' action allows searching for a substring (case ins.)
    of its name via the 'name' url param (/api/categories/?name=<substring>)
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsAdminOrReadOnly,
                         )
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.CategoryListSerializer
        else:
            return serializers.CategorySerializer

    def get_queryset(self):
        substring = self.request.query_params.get('name', None)
        if substring is not None:
            return self.queryset.filter(name__contains=substring.lower())
        else:
            return self.queryset


class ArticleViewSet(viewsets.ModelViewSet):
    """
    this viewset provides 'list' and 'retrieve' actions to everyone.
    'create', 'update' and 'destroy' actions to authors (owners) only.
    The 'list' action allows searching for a substring (case ins.)
    of its title via the 'title' url param (/api/articles/?title=<substring>)
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, 
                          IsAuthorOrReadOnly,
                         )
    queryset = models.Article.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ArticleListSerializer
        else:
            return serializers.ArticleSerializer

    def get_queryset(self):
        substring = self.request.query_params.get('title', None)
        if substring is not None:
            return self.queryset.filter(title__contains=substring.lower())
        else:
            return self.queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    this viewset provides 'list' and 'retrieve' actions only.
    The 'list' action allows searching for a substring (case ins.)
    of its username via the 'username' url param
    (/api/authors/?username=<substring>)
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AuthorListSerializer
        else:
            return serializers.AuthorSerializer

    def get_queryset(self):
        substring = self.request.query_params.get('username', None)
        if substring is not None:
            return self.queryset.filter(username__contains=substring.lower())
        else:
            return self.queryset

