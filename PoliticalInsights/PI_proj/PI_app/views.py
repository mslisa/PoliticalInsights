# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
# import pandas as pd

# django specific imports
from django.shortcuts import render
from django.http import HttpResponseRedirect

# model imports
from .models import Effectiveness
from .forms import UserAddress, SelectRep, SelectMetric
import api_utils#, metric_utils

def home(request):

    # setup default values for return statement
    # returns these values if GET (or any other method)
##    my_reps = {}
##    user_address_form = UserAddress()
##    selected_rep_form = SelectRep()
##    selected_metric_form = SelectMetric()
##    all_reps_effectiveness = Effectiveness.objects.all() #TODO may not be needed?

    
    # if POST request (user entered information) then process form data
    if request.method == 'POST':

        # POST is for user_address; need to find new reps
        if 'user_address' in request.POST:
            
            user_address_form = UserAddress(request.POST)
            
            # retrieve representatives for given address
            # google response is in form:
            #   {chamber:
            #      {rep_id:
            #         {image_url: 'https://...',
            #          name: 'Joe Dirt'
            #         }
            #      }
            #   }
            g = api_utils.Google()
            my_reps = {}
            
            #validate address
            my_reps_g = g.ids_from_address(request.POST['user_address'])
            
            for chamber, member_list in my_reps_g.items():
                for member_id, member_info in member_list.items():
                    my_reps[member_id] = {'chamber': chamber,
                                          'img_url': member_info['img_url'],
                                          'name': member_info['name']
                                          }

            return render(request, 'home.html',
                          {'my_reps': my_reps,
                           'user_address_form': user_address_form,
                           'selected_rep_form': SelectRep(initial={'selected_rep': member_id}),
                           'posted_data':request.POST,
                           'selected_metric_form': SelectMetric(initial={'selected_,metric': 'Contact'})
                           } )
            
        # POST is for selected_rep #TODO they are disappearing https://stackoverflow.com/questions/866272/how-can-i-build-multiple-submit-buttons-django-form
        elif 'selected_rep' in request.POST:
            selected_rep_form = SelectRep(request.POST)
            return render(request, 'home.html',
                          {
                           'user_address_form': UserAddress(),
                           'selected_rep_form': selected_rep_form,
                           'posted_data':request.POST,
                           'selected_metric_form': SelectMetric()
                           } )

        # POST is for selected_metric
        elif 'selected_metric' in request.POST:
            selected_metric_form = SelectMetric(request.POST)
            return render(request, 'home.html',
                          {
                           'user_address_form': UserAddress(),
                           'selected_rep_form': SelectRep(),
                           'posted_data':request.POST,
                           'selected_metric_form': selected_metric_form
                           } )

    return render(request, 'home.html', {'user_address_form': UserAddress()})
