from django import forms
from .models import Course, Module, Lesson, Review


class CourseForm(forms.ModelForm):
    """Form for creating and editing courses."""

    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail', 'category', 'level', 'price', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'thumbnail':
                field.widget.attrs['class'] = 'form-file-input'
            elif field_name == 'is_published':
                field.widget.attrs['class'] = 'form-checkbox'
            else:
                field.widget.attrs['class'] = 'form-input'


class ModuleForm(forms.ModelForm):
    """Form for creating and editing modules."""

    class Meta:
        model = Module
        fields = ['title', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'


class LessonForm(forms.ModelForm):
    """Form for creating and editing lessons."""

    class Meta:
        model = Lesson
        fields = ['title', 'content', 'video_url', 'file', 'order', 'duration_minutes']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'file':
                field.widget.attrs['class'] = 'form-file-input'
            else:
                field.widget.attrs['class'] = 'form-input'


class ReviewForm(forms.ModelForm):
    """Form for submitting course reviews."""

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['class'] = 'form-input'
        self.fields['rating'].widget.attrs['class'] = 'form-input'
