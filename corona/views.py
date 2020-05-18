from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import random
from status.models import CoronaVirusStatus
import time

def get_data(cname):
    url = "https://api.covid19api.com/live/country/{}".format(cname.lower().replace(' ', '-'))
    r = requests.get(url)
    data = r.json()[-1]
    return data

def get_global():
    url = 'https://api.covid19api.com/summary'
    r = requests.get(url)
    data = r.json()['Global']
    return data


def country(request, cname):
    try:
        data = get_data(cname)
        infected = int(data['Confirmed'])
        deaths = int(data['Deaths'])
        recovered = int(data['Recovered'])
        context = {"infected":infected, "deaths":deaths, "recovered":recovered, "country":cname, 'page_url':cname.lower()}
    except:
        infected = '---'
        deaths = '---'
        recovered = '---'
        context = {"infected":infected, "deaths":deaths, "recovered":recovered, "country":f'{cname} which does not exist in our data', 'page_url':cname.lower()}
        return render(request, 'people.html', context)
    try:
        cntry = CoronaVirusStatus.objects.get(country=cname.lower())
        cntry.infected = infected
        cntry.deaths = deaths
        cntry.recovered = recovered
        if f"i:{cntry.infected}, d:{cntry.deaths}. r:{cntry.recovered}" not in cntry.oldinf:
                cntry.oldinf.append(f"i:{cntry.infected}, d:{cntry.deaths}. r:{cntry.recovered}")
        cntry.save()
    except:
        CoronaVirusStatus.objects.create(country=cname.lower(), infected=infected, deaths=deaths, recovered=recovered).save()
    return render(request, 'people.html', context)

def data_from_database(request, cname):
    try:
        obj = CoronaVirusStatus.objects.get(country=cname)
        infected = obj.infected
        deaths = obj.deaths
        recovered = obj.recovered
    except:
        url = "https://epidemic-stats.com/coronavirus/{}".format(cname.lower())
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        h5 = soup.find_all('h5')
        infected = h5[0].get_text()
        deaths = h5[1].get_text().split(' ')[0].replace('\n', '')
        recovered = h5[2].get_text().split(' ')[0]
        
        try:
            cntry = CoronaVirusStatus.objects.get(country=cname.lower())
            cntry.infected = infected
            cntry.deaths = deaths
            cntry.recovered = recovered
            
            if f"i:{cntry.infected}, d:{cntry.deaths}. r:{cntry.recovered}" not in cntry.oldinf:
                cntry.oldinf.append(f"i:{cntry.infected}, d:{cntry.deaths}. r:{cntry.recovered}")
            cntry.save()
        except:
            CoronaVirusStatus.objects.create(country=cname.lower(), infected=infected, deaths=deaths, recovered=recovered).save()  
    context = {"infected":infected, "deaths":deaths, "recovered":recovered, "country":cname, "page_url":cname}
    return render(request, 'people.html', context)


def home(request):
    data = get_global()
    infected = int(data['TotalConfirmed'])
    deaths = int(data['TotalDeaths'])
    recovered = int(data['TotalRecovered'])
    context = {"infected":infected, "deaths":deaths, "recovered":recovered, "country":'The Whole World'}
    return render(request, 'home.html', context)
