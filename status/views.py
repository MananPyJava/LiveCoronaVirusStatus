from django.shortcuts import render

from rest_framework import viewsets

from .serialize import CoronaVirusStatusSerializer
from .models import CoronaVirusStatus


class CoronaVirusStatusViewSet(viewsets.ModelViewSet):
    queryset = CoronaVirusStatus.objects.all().order_by('country')
    serializer_class = CoronaVirusStatusSerializer