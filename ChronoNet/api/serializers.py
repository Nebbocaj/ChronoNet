from rest_framework import serializers
from post.models import Post, Vote
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = User
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", )


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Vote
        fields = ['id', 'post', 'user', 'vote']
