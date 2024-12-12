# blog/forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    class Meta:
        model = Post
        fields = [
            'title', 
            'content', 
            'featured_image', 
            'categories', 
            'tags', 
            'is_published', 
            'meta_description',
            'featured'
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
            'tags': forms.CheckboxSelectMultiple,
        }

class CommentForm(forms.ModelForm):
    """
    Form for posting comments
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your comment here...'}),
        }