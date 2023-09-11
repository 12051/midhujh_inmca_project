from django.contrib import messages
from django.shortcuts import render, redirect
#from .models import User
from .forms import CrimeReportForm
from .models import CustomUser,CrimeReport
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def index(request):
    return render(request,'index.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

def victimregister(request):
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
            user.is_victim=True
            user.save()
            return redirect('/')
    return render(request, 'victimregister.html')

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
            return redirect('reported_crimes')
    else:
        form = CrimeReportForm()
    
    return render(request, 'report_crime.html', {'form': form})

def reported_crimes(request):
    return render(request,'reported_crimes.html')

def generate_pdf(request):
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            form.save()
            template_path = 'reported_crimes.html'  # Replace with your template path
            context = {'form': form}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="fir.pdf"'

            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if not pisa_status.err:
                return response

    else:
        form = CrimeReportForm()

    return render(request, 'report_crime.html', {'form': form})

@login_required
def webinar(request):
# update_webinar = Webinar.objects.all()    
    orgs=request.user
    list_crime=CrimeReport.objects.filter(org_user=orgs)
    context = {'list_crime': list_crime}
    return render(request, 'webinar.html', context)