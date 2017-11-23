# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# django specific imports
from django.shortcuts import render
from django.http import HttpResponseRedirect

# model imports
from .models import Effectiveness
from .forms import UserAddress, SelectRep, SelectMetric
import api_utils, metric_utils

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

def fig_response(fig):
    canvas = FigureCanvas(fig)
    fig_response = HttpResponse(content_type = 'image/png')
    canvas.print_png(fig_response)
    return fig_response

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
            i_rep = request.POST['selected_rep']
        else:
            i_rep = my_reps.keys()[0]
        rendered_data['selected_rep_form'] = SelectRep(my_reps, initial={'selected_rep': i_rep})
        
        # get graphs and figures to display dependent upon metric        
        if metric == 'Contact':
            rendered_data['text_stat'] = {"msg": "You've selected Contact"}
        elif metric == 'Effectiveness':
            df = pd.read_csv('data/effectiveness.csv')
            e = metric_utils.effectiveness()
            fig = e.generate_plot(df, i_rep)     # return plt.figure()
            rendered_data['fig'] = fig_response(fig)
            rendered_data['text_stat'] = e.key_stats(df, i_rep)   # return dictionary
        elif metric == 'Bipartisanship':
            df = pd.read_csv('data/effectiveness.csv')
            b = metric_utils.bipartisanship()
            fig = b.generate_plot(df, i_rep)     # return plt.figure()
            rendered_data['fig'] = fig_response(fig)
            rendered_data['text_stat'] = b.key_stats(df, i_rep)   # return dictionary
        elif metric == 'Financial':
            df = pd.read_csv("findata/fincampaign.csv",header=None)
            f = metric_utils.financials()
            fig = f.fin_plot(df, i_rep)      # return plt.figure()
            rendered_data['fig'] = fig_response(fig)
        elif metric == 'Social':
            df = pd.read_csv('findata/final_twitter_df.csv')
            t = metric_utils.twitter_stuff()
            fig = t.twitter(df, i_rep)      # return plt.figure()
            rendered_data['fig'] = fig_response(fig)          

    return render(request, 'home.html', rendered_data)
