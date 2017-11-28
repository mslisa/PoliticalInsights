# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve

from .views import home

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_invalid_address_shows_error_message(self):
        pass

    def test_valid_address_shows_buttons(self):
        pass

    def test_select_rep_changes_rep(self):
        pass

    def test_select_metric_changes_metric(self):
        pass
