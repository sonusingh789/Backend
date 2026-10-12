from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "body",
            "publish",
            "created",
            "updated",
            "status",
            "author",
            "author_name",
        ]
        read_only_fields = ["id", "created", "updated", "author_name"]
