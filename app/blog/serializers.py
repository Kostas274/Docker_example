from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'posts', 'comments']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    title = serializers.CharField(max_length=120)
    text = serializers.CharField()
    created_date = serializers.DateTimeField()
    published_date = serializers.DateTimeField()

    class Meta:
        model = Post
        fields = ['id', 'owner', 'title', 'text', 'created_date', 'published_date']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.created_date = validated_data.get('created_date', instance.created_date)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.save()
        return instance


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    text = serializers.CharField()
    created_date = serializers.DateTimeField()
    approved_comment = serializers.BooleanField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'owner', 'text', 'created_date', 'approved_comment']
