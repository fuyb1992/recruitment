from dal import autocomplete
from django.forms import ModelForm
from .models import *

class positionsForm(ModelForm):
    class Meta:
        model = positions
        exclude = ('',)
#         widgets = {
#             'category':autocomplete.ModelSelect2(url='position_category-autocomplete'),
#         }