# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# This is the basic setup of the supporting database

class Effectiveness(models.Model):
    rep_id = models.CharField(max_length=7)
    bi_sponsor_bi = models.IntegerField
    bi_sponsor_count = models.IntegerField
    cosponsor_count = models.IntegerField
    cosponsor_normalized = models.FloatField
    cosponsor_rank = models.IntegerField
    dw_nominate = models.FloatField
    missed_votes_pct = models.FloatField
    name = models.CharField(max_length=99)
    party = models.CharField(max_length=1)
    seniority = models.IntegerField
    sponsor_count = models.IntegerField
    sponsor_normalized = models.FloatField
    sponsor_rank = models.IntegerField
    state = models.CharField(max_length=2)
    top_cosponsor_subjects = models.CharField(max_length=500)
    top_sponsor_subjects = models.CharField(max_length=500)
    total_votes = models.IntegerField
    votes_with_party_pct = models.FloatField
    color = models.CharField(max_length=50)
    size = models.IntegerField
    bi_pct = models.FloatField
    chamber = models.CharField(max_length=50)
    congress = models.IntegerField

    def __str__(self):
        return "{} {} ({}), congress {}".format(self.chamber,
                                                self.name,
                                                self.party,
                                                self.congress)
