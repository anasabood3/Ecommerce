from typing import Counter
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.utils.translation import ugettext as _



class ProductSearchForm(forms.Form):
    q = forms.CharField()