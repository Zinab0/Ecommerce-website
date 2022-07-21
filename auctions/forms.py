from django import forms
from django.forms import ModelForm, widgets
from .models import *
from django import forms


class ListingsForm(forms.ModelForm):
     class Meta:
        model = Listings
        fields = { 'title','picture','price','description','category'}
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control','placeholder':'Attractive title...'}),
            'picture' : widgets.FileInput(attrs={'class' : 'form-control'}),
            'price' : widgets.NumberInput(attrs={'class' : 'form-control'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control'}),
            'category' : forms.Select(attrs={'class' : 'form-control'}),

        }

class BiddingForm(ModelForm):
     class Meta:
        model = Bid
        fields = '__all__' 
        widgets = {
            'user':widgets.TextInput(attrs={'class' : 'form-control'}),
            'listing':widgets.Input(attrs={'class' : 'form-control'}),
            'price' : widgets.NumberInput(attrs={'class' : 'form-control'}),
        }

class CommentForm(forms.ModelForm):
     class Meta:
        model = Comment
        fields = {'comment', }
        widgets = {
            'comment':forms.Textarea(attrs={'class' : 'form-control','placeholder':'Be polite...'}),
        }