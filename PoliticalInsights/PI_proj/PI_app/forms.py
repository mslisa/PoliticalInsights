# form for submitting information from the website to the server
# basic path is url--{address, rep, metric}-->server
# with a return of url<--{metric supply}--server

from django import forms
from .models import Effectiveness

class UserAddress(forms.Form):
    user_address = forms.CharField(label='Your address', strip=True)

class SelectRep(forms.Form):
    selected_rep = forms.CharField(strip=True)

class SelectMetricType(forms.Form):
    selected_metric = forms.CharField(strip=True)
