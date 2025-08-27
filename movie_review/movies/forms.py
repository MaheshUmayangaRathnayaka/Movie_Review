from django import forms
from .models import Comment, Movie
# from .models import Movie

common_class = "mb-5 mt-2 text-gray-600 focus:outline-none focus:border focus:border-pgreen font-normal w-full h-10 flex items-center pl-3 text-sm border-gray-300 rounded border"
          



class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs.update({
            'class': "text-gray-600 focus:outline-none focus:border focus:border-pgreen font-normal w-full flex items-center p-3 text-base rounded border"
        })

    class Meta:
        model = Comment
        fields = ('comment',)
        labels = {"comment" : ("Change your comment below"),}

class MovieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

        CHOICES = (
            ('Action', 'Action'),
            ('Comedy', 'Comedy'),
            ('Sci-Fi', 'Sci-Fi'),
            ('Adventure', 'Adventure'),
            ('Drama', 'Drama')
        )

        self.fields['title'].widget.attrs.update({
            'class': common_class        
        })
        self.fields['image'].widget.attrs.update({
            'class': common_class        
        })
        self.fields['producer'].widget.attrs.update({
            'class': common_class        
        })
        self.fields['year'].widget.attrs.update({
            'class': common_class        
        })
        self.fields['category'].widget = forms.Select(
            choices=CHOICES,
            attrs={
                'class': "mb-5 mt-2 text-gray-600 focus:outline-none focus:border focus:border-pgreen font-normal w-full h-10 flex items-center pl-3 text-sm border-gray-300 rounded border"
            }
        )
        self.fields['description'].widget.attrs.update({
            'class': common_class,        
        })

    class Meta:
        model = Movie 
        fields = ('title', 'image', 'producer', 'year', 'category', 'description')      