
from django import forms
from .models import Book,User

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publication_year']

class AddUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','user_type']
