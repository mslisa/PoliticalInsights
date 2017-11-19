# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
# import pandas as pd

# django specific imports
from django.shortcuts import render
from django.http import HttpResponseRedirect

# model imports
from .models import Effectiveness
from .forms import UserAddress, SelectRep, SelectMetricType
import api_utils

def home(request):

    # setup default values for return statement
    # returns these values if GET (or any other method)
    my_reps = {}
    user_address_form = UserAddress()
    selected_rep_form = SelectRep()
    selected_metric_form = SelectMetricType()
    all_reps_effectiveness = Effectiveness.objects.all() #TODO may not be needed?

    
    # if POST request (user entered information) then process form data
    if request.method == 'POST':
        user_address = request.POST['user_address']
        
        # user address in POST      # TODO-make this into the address widget
        if user_address != '':
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
            my_reps_g = g.ids_from_address(user_address)
            
            for chamber, member_list in my_reps_g.items():
                for member_id, member_info in member_list.items():
                    my_reps[member_id] = {'chamber': chamber,
                                          'img_url': member_info['img_url'],
                                          'name': member_info['name']
                                          }

            # reset SelectRep and SelectMetric
            selected_rep_form = SelectRep()
            selected_metric_form = SelectMetricType()

        # rep selected in POST
        elif 'selected_rep' in request.POST:
            selected_rep_form = SelectRep(request.POST)

        # metric selected in POST
        elif 'selected_metric' in request.POST:
            selected_metric_form = SelectMetricType(request.POST)

    
    return render(request,
                  'home.html',
                  {'my_reps': my_reps,
                   'user_address_form': user_address_form,
                   'selected_rep_form': selected_rep_form,
                   'selected_metric_form': selected_metric_form
                  },
                 )
