from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# Define a custom widget for text input fields
class CustomTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500',
            'placeholder': kwargs.get('placeholder', ''),
        }
        super().__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=CustomTextInput(attrs={'placeholder': 'Type product name'}))
    # Define other fields as necessary, using the custom widget

    class Meta:
        model = Post
        fields = ['title', 'image', 'body', 'category', 'tags']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500', 'placeholder': 'Upload a featured image for the post'}),
            'body': CKEditorUploadingWidget(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500', 'placeholder': 'Enter the body of the post'}),
            'category': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500', 'placeholder': 'Select category'}),
            'tags': forms.SelectMultiple(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-600 focus:border-gray-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-gray-500 dark:focus:border-gray-500', 'placeholder': 'Select tags'}),
        }
        labels = {
            'title': 'Title',
            'image': 'Image',
            'body': 'Body',
            'category': 'Category',
            'tags': 'Tags',
        }
        help_texts = {
            'title': 'Enter the title of the post',
            'image': 'Upload a featured image for the post',
            'body': 'Enter the body of the post',
            'category': 'Select a category for the post',
            'tags': 'Select tags for the post',
        }
        error_messages = {
            'title': {
                'max_length': 'The title is too long',
            },
        }
