from pyexpat import model
from typing import Counter
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,SetPasswordForm,PasswordChangeForm)
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField, ImageField
from django.forms.models import inlineformset_factory
from store.models import Category, Offer, Product, ProductImage, ProductSpecificationValue,ProductType,ProductSpecification
from django.utils.translation import ugettext as _

#-------------Category Forms-------------------
class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Category Name',min_length=4,max_length=60)
    cover = forms.ImageField(label='Cover Image')
    # parent= forms.ChoiceField(label='Category',required=False)
    is_active = forms.BooleanField(label='Status',help_text='Control yor product vissablity on the store')

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control form-control-md'})
        self.fields['parent'].widget.attrs.update({'class':'form-control form-control-md'})
        self.fields['cover'].widget.attrs.update({'class':'custom-file-input'})
        self.fields['is_active'].widget.attrs.update({'class':'form-control form-control-sm'})

    class Meta:
        model = Category
        fields = ('name','cover','is_active','parent')

#---------Product Forms------------
#Manage Product Form
class ProductForm(forms.ModelForm):

    title = forms.CharField(label='Title', min_length=4, max_length=255)
    # category = forms.ChoiceField(label='Category',)
    # product_type = forms.ChoiceField(label="Product Type")
    description = forms.CharField(label='Description')
    regular_price = CharField(label="Formal Price")
    discount_price = forms.CharField(label='Descounted Price')
    is_active = forms.BooleanField(label='Status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Product Title', 'id': 'form-product_name'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['product_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['regular_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount_price'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-control'})
        
    class Meta:
        model = Product
        fields = ('title','category','product_type','description','regular_price','discount_price','is_active',)




class ProductSpecificationValueForm(forms.ModelForm):
    def get_product(self):
        return self.cleaned_data['product']

    # specification = forms.ModelChoiceField(queryset=ProductSpecification.objects.filter(product_type=1))

    
    class Meta:
        model=ProductSpecificationValue
        fields = ('specification','value')

ProductSpecsFormset = inlineformset_factory(Product,  # parent form
                                                  ProductSpecificationValue,  # inline-form
                                                  form=ProductSpecificationValueForm,
                                                #   fields=['specification','value'], # inline-form fields
                                                  # labels for the fields
                                                  widgets = {'value': forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Product Type Name'})},
                                                  labels={
                                                        'specification': _(u'Specification:'),
                                                        'value': _(u'Value:'),
                                                  },
                                                 # help texts for the fields
                                                  help_texts={'specification':None,'value': None,},
                                                   # set to false because cant' delete an non-exsitant instance
                                                  can_delete=True,
                                                  # how many inline-forms are sent to the template by default
                                                  extra=2,
                                                  )

ProductImagesFormset = inlineformset_factory(Product,  # parent form
                                                  ProductImage,  # inline-form
                                                  fields=['image','is_feature','alt_text'], # inline-form fields
                                                  # labels for the fields
                                                
                                                  labels={
                                                        'image': _(u'Image:'),
                                                        'alt_text': _(u'Alt Text:'),
                                                        'is_feature': _(u'Cover Image:'),
                                                  },
                                                  # help texts for the fields
                                                  help_texts={'image':None,'alt_text': None,'is_feature': None,},
                                                  # set to false because cant' delete an non-exsitant instance
                                                  can_delete=True,
                                                  # how many inline-forms are sent to the template by default
                                                  extra=2
                                                  )


#---------Product Types Forms------------
class ProductTypeForm(forms.ModelForm):
    name = forms.CharField(label="Name")
    is_active = forms.BooleanField(label="Status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-md'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-control form-control-md'})
    
    class Meta:
        model = ProductType
        fields = ['name','is_active']


ProductTypeFormset = inlineformset_factory(ProductType,  # parent form
                                                  ProductSpecification,  # inline-form
                                                  fields=['name'], 
                                                  widgets = {'name': forms.TextInput(attrs = {'class': 'form-control form-control-md', 'placeholder': 'Product Specification Name'})},
                                                  labels={
                                                        'name': _(u'Name:'),
                                                  },
                                                  help_texts={
                                                        'name': None,
                                                  },
                                                  can_delete=True,
                                                  extra=0
                                                  )




class OfferForm(forms.ModelForm):
    title = forms.CharField(label='Title', min_length=4, max_length=255)
    description = forms.CharField(label='Description')
    image = ImageField(label='Cover Image')
    is_active = forms.BooleanField(label='Status',help_text='Control yor product vissablity on the store',required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].widget.attrs.update({'class':'form-control form-control-lg'})
        self.fields['description'].widget.attrs.update({'class':'form-control form-control-lg'})
        self.fields['image'].widget.attrs.update({'class':'form-control form-control-lg'})
        self.fields['is_active'].widget.attrs.update({'class':'form-control form-control-sm'})
 
    class Meta:
        model = Offer
        fields=['title','description','image','is_active']