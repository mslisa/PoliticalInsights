# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
# import pandas as pd

# django specific imports
from django.shortcuts import render

# model imports
from .models import Effectiveness
import api_utils

def home(request):
    
    # identify user address
    address = "1313 Disneyland Dr, Anaheim, CA 92802" #TODO - get user input as address

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
    my_reps_g = g.ids_from_address(address)
    my_reps = {}
    for chamber, member_list in my_reps_g.items():
        for member_id, member_info in member_list.items():
            my_reps[member_id] = {'chamber': chamber,
                                  'img_url': member_info['img_url'],
                                  'name': member_info['name']
                                  }
    #        print "chamber: {}".format(member_info['name'])
    #        display(Image(url=member_info['image_url'], height=165, width=135))
            
    all_reps_effectiveness = Effectiveness.objects.all()
    return render(request,
                  'home.html',
                  {'effectiveness': all_reps_effectiveness, 'my_reps': my_reps}
                  )
