# form for submitting information from the website to the server
# basic path is url--{address, rep, metric}-->server
# with a return of url<--{metric supply}--server

import pandas as pd
from django import forms
from .models import Effectiveness
import api_utils

class UserAddress(forms.Form):
    user_address = forms.CharField(widget=forms.TextInput(attrs={'size':80}),
                                   label='Please enter your address',
                                   strip=True)    

class SelectRep(forms.Form):
    def __init__(self, my_reps, *args, **kwargs):
        super(SelectRep, self).__init__(*args, **kwargs)
        self.fields['selected_rep'] = forms.ChoiceField(
            choices=[(rep_id, rep_key) for rep_id, rep_key in my_reps.items()],
            widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit();', 
                                            'id': 'value'})
            )

class SelectMetric(forms.Form):
    def __init__(self, metrics, *args, **kwargs):
        super(SelectMetric, self).__init__(*args, **kwargs)
        self.fields['selected_metric'] = forms.ChoiceField(
            choices=[(m, m) for m in metrics],
            widget=forms.RadioSelect(attrs={'onchange': 'this.form.submit();'})
            )
