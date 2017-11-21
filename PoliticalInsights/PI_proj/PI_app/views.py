# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
import pandas as pd

# django specific imports
from django.shortcuts import render
from django.http import HttpResponseRedirect

# model imports
from .models import Effectiveness
from .forms import UserAddress, SelectRep, SelectMetric
import api_utils#, metric_utils

def get_reps(user_address):
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

    #TODO validate address
    my_reps_g = g.ids_from_address(user_address)

    for chamber, member_list in my_reps_g.items():
        for member_id, member_info in member_list.items():
            my_reps[member_id] = {'chamber': chamber,
                                  'img_url': member_info['img_url'],
                                  'name': member_info['name']
                                  }

    return my_reps
    

def home(request):

    # initialize return data
    # use POSTed data if available, otherwise use an empty form
    rendered_data = {'user_address_form': UserAddress(request.POST \
                                                      if request.method == 'POST' \
                                                      else None)}
    
    # if POST request (user entered information) then process form data
    if request.method == 'POST':

        # TODO delete this and make sure it's out of html. Dev only.
        rendered_data['posted_data']=request.POST

        # used POSTed metric otherwise initialize to Contact
        if 'selected_metric' in request.POST:
            metric = request.POST['selected_metric']
        else:
            metric = 'Contact'
        rendered_data['selected_metric_form'] = SelectMetric(initial={'selected_metric': metric})
        
        # used POSTed rep otherwise initialize to any rep
        my_reps = get_reps(request.POST['user_address'])
        rendered_data['my_reps'] = my_reps
        if 'selected_rep' in request.POST:
            initial_rep = request.POST['selected_rep']
        else:
            initial_rep = my_reps.keys()[0]
        rendered_data['selected_rep_form'] = SelectRep(my_reps, initial={'selected_rep': initial_rep})
        
        # get graphs and figures to display dependent upon metric
        # TODO pull in metric_utils
            

    return render(request, 'home.html', rendered_data)
