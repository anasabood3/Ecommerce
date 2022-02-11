from typing import Counter
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.utils.translation import ugettext as _
from mptt.forms import TreeNodeChoiceField
from .models import Comment

class ProductSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['q'].label='Search For'
        self.fields['q'].widget.attrs.update({
            'class':'form-control mr-sm-2',
            'placeholder':'find a product'
        })
        self.fields['q'].widget.attrs.update(
            {'data-toggle':'dropdown'}
        )

class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    class Meta:
        model = Comment
        fields = ('content','parent',)
        wedgits = {
            "content":forms.Textarea(attrs={"class":"form-control"}),
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['parent'].required=False
        self.fields['parent'].widget.attrs.update(
            {'class':'d-none'}
        )