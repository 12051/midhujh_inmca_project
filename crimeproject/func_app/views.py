from django.shortcuts import render

from crimeapp.models import CrimeReport, PublicReport
from .models import Advocate  # Importing the Advocate model

def advocate_detail(request, act):
    data = CrimeReport.objects.filter(id=act)
    print(data)
    if data.exists():
        status = data[0].location_status # Assuming 'reporter_location' is the correct field name
        print(status)
        advocates = Advocate.objects.filter(office_place=status)
        print(advocates)
    else:
        advocates = Advocate.objects.all()

    return render(request, 'view_advocate.html', {'advocate': advocates})

def advocate_public(request, act):
    data = PublicReport.objects.filter(id=act)
    print(data)
    if data.exists():
        status = data[0].location_status # Assuming 'reporter_location' is the correct field name
        print(status)
        advocates = Advocate.objects.filter(office_place=status)
        print(advocates)
    else:
        advocates = Advocate.objects.all()

    return render(request, 'view_advocate.html', {'advocate': advocates})
