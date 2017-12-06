# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Basic python imports
import pandas as pd
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# django specific imports
from django.shortcuts import render
from django.http import HttpResponse

# model imports
from .models import Effectiveness
from .forms import UserAddress, SelectRep, SelectMetric
import api_utils, metric_utils

import logging

logger = logging.getLogger(__name__)

#fig_dict = {‘fig’: fig_object, ‘fig_explanation’: “blah blah about fig_object”}
#quick_stat_dict = {‘stat1’: {‘stat’:big_number_stat, ‘stat_explanation’: “blah blah about big_number_stat”}, ’stat2’: …}

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

    # get google response
    my_reps_g = g.ids_from_address(user_address)
       
    for chamber, member_list in my_reps_g.items():
        for member_id, member_info in member_list.items():
            my_reps[member_id] = {'chamber': chamber,
                                  'official_title': get_title(chamber),
                                  'img_url': member_info['img_url'],
                                  'name': member_info['name']
                                  }

    return my_reps

def home(request):

    logger.error('LISA: 10 logger mark')

    # initialize return data
    # use POSTed data if available, otherwise use an empty form
    rendered_data = {'user_address_form': UserAddress(request.POST \
                                                      if request.method == 'POST' \
                                                      else None)}
    
    # if POST request (user entered information) then process form data
    if request.method == 'POST':

        #### USER ADDRESS ###

        # check that address is valid
        logger.error('LISA: 20 logger mark')
        if len(request.POST['user_address']) < 5:
            rendered_data['error_message'] = 'Address not found. Please try again.'
            return render(request, 'home.html', rendered_data)
        try:
            my_reps = get_reps(request.POST['user_address'])
        except:
            rendered_data['error_message'] = 'Address not found. Please try again.'
            return render(request, 'home.html', rendered_data)
        
        #### REPRESENTATIVES ###

        # used POSTed rep otherwise initialize to any rep
        logger.error('LISA: 30 logger mark')
        rendered_data['my_reps'] = my_reps
        if 'selected_rep' in request.POST:
            i_rep = request.POST['selected_rep']
        else:
            i_rep = my_reps.keys()[0]
        rendered_data['i_rep'] = i_rep
        rendered_data['i_rep_name'] = my_reps[i_rep]['name']
        # TODO: add in party affiliation
        rendered_data['selected_rep_form'] = SelectRep(my_reps, initial={'selected_rep': i_rep})

        # TODO delete this and make sure it's out of html. Dev only.
        rendered_data['posted_data']=request.POST

        #### METRICS ###

        # used POSTed metric otherwise initialize to Contact
        logger.error('LISA: 40 logger mark')
        metrics = ['Contact', 'Effectiveness']#, 'Bipartisanship', 'Financial', 'Social']
        if 'selected_metric' in request.POST:
            metric = request.POST['selected_metric']
        else:
            metric = 'Contact'
        rendered_data['metric'] = metric
        rendered_data['selected_metric_form'] = SelectMetric(metrics, initial={'selected_metric': metric})
        logger.error('LISA: 40 {}'.format(metric))

        df = ''

        # get metric text to display dependent upon metric (figure comes from metric_graph function)     
        if metric == 'Contact':
            logger.error('LISA: 50con logger mark')
            contact = metric_utils.contact()
            logger.error('LISA: 51con logger mark')
            contact_dict = contact.contact_card('data/contact_file.json', i_rep)
            logger.error('LISA: 52con logger mark')
            rendered_data['quick_stat_dict'] = contact_dict
            
        elif metric == 'Effectiveness':
            logger.error('LISA: 50eff logger mark')
            metric_obj = metric_utils.effectiveness()
            logger.error('LISA: 51eff logger mark')
            fig_dict = metric_obj.generate_plot(i_rep)
            logger.error('LISA: 52eff logger mark')
            rendered_data['fig_explanation'] = fig_dict['fig_explanation']
            logger.error('LISA: 53eff logger mark')
            quick_stat_dict = metric_obj.key_stats(i_rep)
            logger.error('LISA: 54eff logger mark')
            rendered_data['quick_stat_dict'] = quick_stat_dict
            logger.error('LISA: 55eff logger mark')

            # df = pd.read_csv('data/effectiveness.csv')
            # metric_obj = metric_utils.effectiveness()

            # # figure
            # fig_dict = metric_obj.generate_plot(df, i_rep)     # return fig_dict (see structure at top)
            # rendered_data['fig_explanation'] = fig_dict['fig_explanation']
            
            # #quick statistics (like big number graphs)
            # quick_stat_dict = metric_obj.key_stats(df, i_rep)   # return quick_stat_dict (see structure at top)
            # rendered_data['quick_stat_dict'] = quick_stat_dict
            
        elif metric == 'Bipartisanship':
            logger.error('LISA: 50bip logger mark')
            # df = pd.read_csv('data/effectiveness.csv')
            metric_obj = metric_utils.bipartisanship()

            # figure
            fig_dict = metric_obj.generate_plot(df, i_rep)     # return fig_dict (see structure at top)
            rendered_data['fig_explanation'] = fig_dict['fig_explanation']
            
            #quick statistics (like big number graphs)
            quick_stat_dict = metric_obj.key_stats(df, i_rep)   # return quick_stat_dict (see structure at top)
            rendered_data['quick_stat_dict'] = quick_stat_dict
            
        elif metric == 'Financial':
            logger.error('LISA: 50fin logger mark')
            # df = pd.read_csv("data/fincampaign_w_twitter.csv", header=None)
            financials = metric_utils.financials()
            metric_obj = financials.fin_plot(df, i_rep) # return dict{'fig_dict', 'quick_stat_dict'}

            # figure
            fig_dict = metric_obj['fig_dict']     # return fig_dict (see structure at top)
            rendered_data['fig_explanation'] = fig_dict['fig_explanation']
            
            #quick statistics (like big number graphs)
            quick_stat_dict = metric_obj['quick_stat_dict']   # return quick_stat_dict (see structure at top)
            rendered_data['quick_stat_dict'] = quick_stat_dict
            
        elif metric == 'Social':
            logger.error('LISA: 50soc logger mark')
            # df = pd.read_csv('data/final_twitter_df.csv')
            twitter = metric_utils.twitter_stuff()
            metric_obj = twitter.twitter(df, i_rep) # return dict{'fig_dict', 'quick_stat_dict'}

            # figure
            fig_dict = metric_obj['fig_dict']     # return fig_dict (see structure at top)
            rendered_data['fig_explanation'] = fig_dict['fig_explanation']
            
            #quick statistics (like big number graphs)
            quick_stat_dict = metric_obj['quick_stat_dict']   # return quick_stat_dict (see structure at top)
            rendered_data['quick_stat_dict'] = quick_stat_dict
                    
    logger.error('LISA: 60  logger mark')
    return render(request, 'home.html', rendered_data)

def metrics_graph(request):
    logger.error('LISA: 100  logger mark')
    metric = request.GET['metric']
    rep_id = request.GET['rep_id']

    df = ''

    if metric == 'Contact':
        logger.error('LISA: 110con  logger mark')
        # if contact, don't return a figure
        return HttpResponse("")
        
    elif metric == 'Effectiveness':
        logger.error('LISA: 110eff  logger mark')
        metric_obj = metric_utils.effectiveness()

        # figure
        logger.error('LISA: 111eff  logger mark')
        fig_dict = metric_obj.generate_plot(rep_id)     # return fig_dict (see structure at top)
        logger.error('LISA: 112eff  logger mark')
        fig = fig_dict['fig']
        # df = pd.read_csv('data/effectiveness.csv')
        # metric_obj = metric_utils.effectiveness()

        # # figure
        # fig_dict = metric_obj.generate_plot(df, rep_id)     # return fig_dict (see structure at top)
        # fig = fig_dict['fig']
        
    elif metric == 'Bipartisanship':
        logger.error('LISA: 110bip  logger mark')
        # df = pd.read_csv('data/effectiveness.csv')
        metric_obj = metric_utils.bipartisanship()

        # figure
        fig_dict = metric_obj.generate_plot(df, rep_id)     # return fig_dict (see structure at top)
        fig = fig_dict['fig']
        
    elif metric == 'Financial':
        logger.error('LISA: 110fin  logger mark')
        # df = pd.read_csv("data/fincampaign_w_twitter.csv", header=None)
        financials = metric_utils.financials()
        metric_obj = financials.fin_plot(df, rep_id) # return dict{'fig_dict', 'quick_stat_dict'}

        # figure
        fig_dict = metric_obj['fig_dict']     # return fig_dict (see structure at top)
        fig = fig_dict['fig']
        
    elif metric == 'Social':
        logger.error('LISA: 110soc  logger mark')
        # df = pd.read_csv('data/final_twitter_df.csv')
        twitter = metric_utils.twitter_stuff()
        metric_obj = twitter.twitter(df, rep_id) # return dict{'fig_dict', 'quick_stat_dict'}

        # figure
        fig_dict = metric_obj['fig_dict']     # return fig_dict (see structure at top)
        fig = fig_dict['fig']


    # process figure for url pass
    # logger.error('LISA: 120  logger mark')
    # canvas = FigureCanvas(fig)
    # logger.error('LISA: 130  logger mark')
    # fig_response = HttpResponse(content_type = 'image/png')
    # logger.error('LISA: 140  logger mark')
    # canvas.print_png(fig_response)
    # logger.error('LISA: 150  logger mark')
    return fig_response

def charts_graph(request):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure(figsize=(4,4))
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
    ax.annotate('rep: {}'.format(request.GET['rep_id']), xy=(x[1], y[1]), xytext=(x[1], y[1]))

    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

def about_view(request):
    HttpResponse("testing about view")
    return render(request, 'index.html')

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