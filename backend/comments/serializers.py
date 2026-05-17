# comments/serializers.py
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content_item', 'user_name', 'user_email', 'comment_text', 
                  'is_question', 'parent_comment', 'replies', 'created_at']
        read_only_fields = ['created_at', 'is_approved']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []