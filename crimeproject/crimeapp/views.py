from django.contrib import messages
from django.shortcuts import render, redirect
#from .models import User
from .forms import CrimeReportForm, AnonyReportForm
from .models import CustomUser,CrimeReport
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request,'index.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def userregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        aadhaar = request.POST.get('aadhaarno')
        password = request.POST.get('password')
        cpwd = request.POST.get('cpd')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif password != cpwd:
            messages.error(request, "Password does not match!")
        elif name and email and aadhaar and password:
            user = CustomUser(name=name,aadhaarno=aadhaar, email=email)
            user.set_password(password)
            user.save()
            return redirect('/')
    return render(request, 'userregister.html')

def witnessregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        aadhaar = request.POST.get('aadhaarno')
        password = request.POST.get('password')
        cpwd = request.POST.get('cpd')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif password != cpwd:
            messages.error(request, "Password does not match!")
        elif name and email and aadhaar and password:
            user = CustomUser(name=name,aadhaarno=aadhaar, email=email)
            user.set_password(password)
            user.is_witness=True
            user.save()
            return redirect('/')
    return render(request, 'witnessregister.html')
    
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    messages.error(request, "Incorrect password")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Email not registered")
        else:
            messages.error(request, "Please provide both email and password")
    return render(request,'login.html')

def report_crime(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CrimeReportForm()
    
    return render(request, 'report_crime.html', {'form': form})

def reported_crimes(request):
    return render(request,'reported_crimes.html')

def generate_pdf(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            cr=form.save(commit=False)
            cr.list_user=request.user
            cr.save()
            crime_report = form.save()
            fir_id = crime_report.id
            template_path = 'reported_crimes.html'  # Replace with your template path
            context = {'form': form, 'fir_id': fir_id}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="FIR_{fir_id}.pdf"'  # Use f-string to include fir_id

            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if not pisa_status.err:
                return response
            return redirect('/')
    else:
        form = CrimeReportForm()

    return render(request, 'index.html', {'form': form})

def about(request):
    return render(request,'about.html')

def general(request):
    return render(request,'general.html')

def laws(request):
    return render(request,'laws.html')

def contact(request):
    return render(request,'contact.html')

def gallery(request):
    return render(request,'gallery.html')

def anony_report(request):
    return render(request,'anony_report.html')

def anony_pdf(request):
    if request.method == 'POST':
        form = AnonyReportForm(request.POST)
        if form.is_valid():
            anony_report = form.save()
            fir_id = anony_report.id
            template_path = 'reported_crimes.html'
            context = {'form': form, 'fir_id': fir_id}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="FIR_{fir_id}.pdf"'  # Use f-string to include fir_id

            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if not pisa_status.err:
                return response

    else:
        form = AnonyReportForm()

    return render(request, 'anony_report.html', {'form': form})

@login_required
def listcrime(request):
    user_crime=request.user
    list_dict=CrimeReport.objects.filter(list_user=user_crime)
    return render(request, 'listcrime.html', {'list_dict': list_dict})

def law_index(request):
    return render(request,'law_index.html')

def law_login(request):
    return render(request,'law_login.html')

def law_update_status(request, crime_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        crime_report = CrimeReport.objects.get(pk=crime_id)
        crime_report.status = new_status
        crime_report.save()
        return redirect('list_crimes')

def update_crime_status(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_id')
        status = request.POST.get('status')

        # Update the status in your database for the specified crime_id
        try:
            crime = CrimeReport.objects.get(pk=crime_id)
            crime.status = status
            crime.save()
            return JsonResponse({'success': True})
        except CrimeReport.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Crime report not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})