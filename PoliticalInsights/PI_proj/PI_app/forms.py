# form for submitting information from the website to the server
# basic path is url--{address, rep, metric}-->server
# with a return of url<--{metric supply}--server

from django import forms
from .models import Effectiveness

import api_utils

class UserAddress(forms.Form):
    user_address = forms.CharField(widget=forms.TextInput(attrs={'size':80}),
                                   label='Please enter your address',
                                   strip=True)    

class SelectRep(forms.Form):
    selected_rep = forms.ChoiceField(widget=forms.RadioSelect)

class SelectMetric(forms.Form):
    METRICS = [('Effectiveness', 'Effectiveness'),
               ('Bipartisanship', 'Bipartisanship'),
               ('Contact', 'Contact')]
    selected_metric = forms.ChoiceField(widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit();'}), choices=METRICS)
