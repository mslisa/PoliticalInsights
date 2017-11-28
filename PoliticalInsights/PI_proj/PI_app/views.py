# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# django specific imports
from django.shortcuts import render
from django.http import HttpResponse

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

    def get_title(chamber):
        if chamber == 'house':
            return "Representative"
        elif chamber == 'senate':
            return "Senator"
        else:
            return None

    #TODO validate address
    my_reps_g = g.ids_from_address(user_address)
       
    for chamber, member_list in my_reps_g.items():
        for member_id, member_info in member_list.items():
            my_reps[member_id] = {'chamber': chamber,
                                  'official_title': get_title(chamber),
                                  'img_url': member_info['img_url'],
                                  'name': member_info['name']
                                  }

    return my_reps

def fig_response(fig):
    canvas = FigureCanvas(fig)
    fig_response = HttpResponse(content_type = 'image/png')
    canvas.print_png(fig_response)
    return fig_response
    #fig_dict = {‘fig’: fig_object, ‘fig_explanation’: “blah blah about fig_object”}
    #quick_stat_dict = {‘stat1’: {‘stat’:big_number_stat, ‘stat_explanation’: “blah blah about big_number_stat”}, ’stat2’: …} # maybe have this as an ordered dict?


def home(request):

    # initialize return data
    # use POSTed data if available, otherwise use an empty form
    rendered_data = {'user_address_form': UserAddress(request.POST \
                                                      if request.method == 'POST' \
                                                      else None)}
    
    # if POST request (user entered information) then process form data
    if request.method == 'POST':

        # check that address is valid
        try:
            my_reps = get_reps(request.POST['user_address'])
        except:
            rendered_data['error_message'] = 'Address not found. Please try again.'
            return render(request, 'home.html', rendered_data)
        
        # used POSTed rep otherwise initialize to any rep
        rendered_data['my_reps'] = my_reps
        if 'selected_rep' in request.POST:
            i_rep = request.POST['selected_rep']
        else:
            i_rep = my_reps.keys()[0]
        rendered_data['i_rep'] = i_rep
        rendered_data['selected_rep_form'] = SelectRep(my_reps, initial={'selected_rep': i_rep})

        # TODO delete this and make sure it's out of html. Dev only.
        rendered_data['posted_data']=request.POST

        # used POSTed metric otherwise initialize to Contact
        if 'selected_metric' in request.POST:
            metric = request.POST['selected_metric']
        else:
            metric = 'Contact'
        rendered_data['metric'] = metric
        rendered_data['selected_metric_form'] = SelectMetric(initial={'selected_metric': metric})
        
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
def chart_get_function(request):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    ax.annotate('metric: {}'.format(request.GET['metric']), xy=(x[0], y[0]), xytext=(x[0], y[0]))
    ax.annotate('metric: {}'.format(request.GET['rep_id']), xy=(x[1], y[1]), xytext=(x[1], y[1]))

    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

# file charts.py
def simple_chart(request):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def dump_request(request):
    from django.http import HttpResponse
    r = HttpResponse(content_type="text/plain")
    r.write("Here is the request:\r\n")
    r.write(dir(request))
    r.write("\r\n:METHOD: ")
    r.write(request.method)
    r.write("\r\nGET:\r\n")
    r.write(dir(request.GET))
    r.write("\r\nGET keys:\r\n")
    for k,v in request.GET.items():
        r.write("{}={}\r\n".format(k,v))

    return r

# http://www.extragravity.com/blog/2014/01/04/matplotlib-django/
# import sys
# from django.http import HttpResponse
# import matplotlib as mpl
# mpl.use('Agg') # Required to redirect locally
# import matplotlib.pyplot as plt
# import numpy as np
# from numpy.random import rand
# try:
#     # Python 2
#     import cStringIO
# except ImportError:
#     # Python 3
#     import io
# def get_image(request):
#    """
#    This is an example script from the Matplotlib website, just to show 
#    a working sample >>>
#    """
#    N = 50
#    x = np.random.rand(N)
#    y = np.random.rand(N)
#    colors = np.random.rand(N)
#    area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses
#    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
#    """
#    Now the redirect into the cStringIO or BytesIO object >>>
#    """
#    if cStringIO in sys.modules:
#       f = cStringIO.StringIO()   # Python 2
#    else:
#       f = io.BytesIO()           # Python 3
#    plt.savefig(f, format="png", facecolor=(0.95,0.95,0.95))
#    plt.clf()
#    """
#    Add the contents of the StringIO or BytesIO object to the response, matching the
#    mime type with the plot format (in this case, PNG) and return >>>
#    """
#    return HttpResponse(f.getvalue(), content_type="image/png")