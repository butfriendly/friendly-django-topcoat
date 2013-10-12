import logging

from django import http
from django.shortcuts import render, render_to_response

def demo(request, template=None):
    """
    Main example view.
    """
    return render_to_response('topcoat/demo.html')
