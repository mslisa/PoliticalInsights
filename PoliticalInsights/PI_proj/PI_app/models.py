# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
from adaptor.model import CsvModel

# This is the basic setup of the supporting database

def return_empty_dict():
    return dict()

class Effectiveness(models.Model):
    rep_id= models.CharField(max_length=7)
    bi_sponsor_bi= models.IntegerField(default=0)
    bi_sponsor_count= models.IntegerField(default=0)
    cosponsor_count= models.IntegerField(default=0)
    cosponsor_normalized= models.FloatField(default=0)
    cosponsor_rank= models.FloatField(default=0)
    dw_nominate= models.FloatField(default=0)
    missed_votes_pct= models.FloatField(default=0)
    name= models.CharField(max_length=255, default='')
    party= models.CharField(max_length=1, default='')
    seniority= models.IntegerField(default=0)
    sponsor_count= models.IntegerField(default=0)
    sponsor_normalized= models.FloatField(default=0)
    sponsor_rank= models.FloatField(default=0)
    state= models.CharField(max_length=2, default='NA')
    top_cosponsor_subjects= JSONField(default=return_empty_dict())
    top_sponsor_subjects= JSONField(default=return_empty_dict())
    total_votes= models.IntegerField(default=0)
    votes_with_party_pct= models.FloatField(default=0)
    color= models.CharField(max_length=255, default='white')
    size= models.IntegerField(default=3)
    bi_pct= models.FloatField(default=0)
    chamber= models.CharField(max_length=255, default='')
    congress= models.IntegerField(default=0)


class Social(models.Model):
    rep_id= models.CharField(max_length=7)
    name= models.CharField(max_length=255)
    twitter_handle= models.CharField(max_length=255)
    total_tweeets= models.IntegerField
    pos_tweets= models.IntegerField
    neg_tweets= models.IntegerField
    tweet_text= JSONField

class Finance(models.Model):
    rep_id= models.CharField(max_length=7)
    field1= models.FloatField
    field2= models.FloatField
    name= models.CharField(max_length=255)
    party= models.CharField(max_length=255)
    status= models.CharField(max_length=1)
    field6= models.FloatField
    field7= models.FloatField
    total_from_individuals= models.FloatField
    total_from_pacs= models.FloatField
    field10= models.FloatField
    field11= models.FloatField



    def __str__(self):
        return "{} {} ({}), congress {}".format(self.chamber,
                                                self.name,
                                                self.party,
                                                self.congress)
