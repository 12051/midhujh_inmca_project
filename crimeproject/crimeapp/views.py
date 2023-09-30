from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
#from .models import User
from .forms import CrimeReportForm, AnonyReportForm, DocReportForm, PublicForm
from .models import CustomUser,CrimeReport, DocReport,SpecLoc,FIRFile
import re
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.http import FileResponse
from django.template.loader import get_template


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
        password = request.POST.get('password')
        cpwd = request.POST.get('cpd')
    
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif password != cpwd:
            messages.error(request, "Password does not match!")
        elif name and email and password:
            user = CustomUser(name=name, email=email)
            token = get_random_string(length=32)
            user.verification_token = token
            user.is_verified = False
            user.set_password(password)
            user.is_normal= True
            user.save()
            send_mail(
                'Email Verification',
                f'Click the following link to verify your email: {request.build_absolute_uri("/verify/")}?token={token}',
                'eventoplanneur@gmail.com',
                [email],
                fail_silently=False,
            )

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
            if user is not None and user.is_verified:
                auth_login(request, user)
                if user.is_normal:
                    return redirect('/')
                if user.is_law:
                    return redirect('law_index')
                return redirect('/')
            else:
                try:
                    user = CustomUser.objects.get(email=email)
                    messages.error(request, "Email not Verified or Incorrect password")
                except CustomUser.DoesNotExist:
                    messages.error(request, "Email not registered")
        else:
            messages.error(request, "Please provide both email and password")
    return render(request,'login.html')

def verify(request):
    token = request.GET.get('token')
    user = CustomUser.objects.filter(verification_token=token).first()
    if user:
        user.is_verified = True
        user.verification_token = None
        user.save()
        return redirect('/')  # Redirect to login page after successful verification
    else:
        return render(request, 'invalid_token.html')  # Handle invalid token

def report_crime(request):
    location_options = ["", "Changanassery", "Chethipuzha", "Kangazha", "Karukachal", "Kurichy", "Madappally", "Nedumkunnam", "Payippad", "Thottackad", "Thrikkodithanam", "Vakathanam", "Vazhappally East", "Vazhappally West", "Vazhoor", "Vellavoor", "Cheruvally", "Chirakkadavu", "Edakkunnam", "Elamgulam", "Elikkulam", "Erumeli North", "Erumeli South", "Kanjirappally", "Koottickal", "Koovappally", "Koruthodu", "Manimala", "Mundakkayam"]
    if request.method == 'POST':
        form = CrimeReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.list_user=request.user
            spec_station_name = request.POST['spec_station']
            reporter_location = request.POST['reporter_location']
            spec_locs = SpecLoc.objects.filter(enforcement_loc=spec_station_name)
            for i in spec_locs:
                if i.reporter_loc==reporter_location:
                    instance.spec_location = i
            instance.save()
            crime_report = form.save()
            fir_id = crime_report.id
            template_path = 'report_template.html'  # Path to your PDF template
            context = {'crime_report': crime_report, 'fir_id': fir_id}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Report_{fir_id}.pdf"'

            template = get_template(template_path)
            html = template.render(context)

            # Create PDF document
            pdf_response = pisa.CreatePDF(html, dest=response)

            if not pdf_response.err:
                return response
            return redirect('/')
    else:
        form = CrimeReportForm()
        
    print(form.errors)
    messages.error(request, form.errors)
    
    
    return render(request, 'report_crime.html', {'form': form, 'location_options':location_options})

def reported_crimes(request):
    return render(request,'reported_crimes.html')

# def generate_pdf(request):
#     if request.method == 'POST':
#         form = CrimeReportForm(request.POST)
#         if form.is_valid():
#             cr=form.save(commit=False)
#             cr.list_user=request.user
#             cr.save()
#             crime_report = form.save()
#             fir_id = crime_report.id
#             template_path = 'reported_crimes.html'  # Replace with your template path
#             context = {'form': form, 'fir_id': fir_id}
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="FIR_{fir_id}.pdf"'  # Use f-string to include fir_id

#             template = get_template(template_path)
#             html = template.render(context)

#             pisa_status = pisa.CreatePDF(html, dest=response)
#             if not pisa_status.err:
#                 return response
#             return redirect('/')
#     else:
#         form = CrimeReportForm()

#     return render(request, 'report_crime.html', {'form': form})

def report_doc(request):
    if request.method == 'POST':
        form = DocReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.list_user=request.user
            instance.save()
            doc_report = form.save()
            fir_id = doc_report.id
            template_path = 'doc_template.html'  # Path to your PDF template
            context = {'doc_report': doc_report, 'fir_id': fir_id}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Report_{fir_id}.pdf"'

            template = get_template(template_path)
            html = template.render(context)

            # Create PDF document
            pdf_response = pisa.CreatePDF(html, dest=response)

            if not pdf_response.err:
                return response
            return redirect('/')
    else:
        form = DocReportForm()
        
    print(form.errors)
    messages.error(request, form.errors)
    
    
    return render(request, 'report_doc.html', {'form': form})

    if request.method == 'POST':
        # Process the form submission
        form = DocReportForm(request.POST, request.FILES)  # Use your form if you have one
        if form.is_valid():
            # Create a new DocumentReport object and save it to the database
            report = form.save(commit=False)
            report.user = request.user  # Assuming you have a user associated with the report
            report.save()
            

            # Define the context for your template
            context = {'report': report}
            messages.success(request, 'Your report has been submitted successfully.')
            return redirect('index')  # Redirect to the desired page after successful submission
        else:
            messages.error(request, form.errors)
    else:
        # Render the initial form
        form = DocReportForm() 
    return render(request, 'report_doc.html', {'form': form})


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

def report_public(request):
    location_options = ["", "Changanassery", "Chethipuzha", "Kangazha", "Karukachal", "Kurichy", "Madappally", "Nedumkunnam", "Payippad", "Thottackad", "Thrikkodithanam", "Vakathanam", "Vazhappally East", "Vazhappally West", "Vazhoor", "Vellavoor", "Cheruvally", "Chirakkadavu", "Edakkunnam", "Elamgulam", "Elikkulam", "Erumeli North", "Erumeli South", "Kanjirappally", "Koottickal", "Koovappally", "Koruthodu", "Manimala", "Mundakkayam"]
    if request.method == 'POST':
        form = PublicForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.list_user=request.user
            spec_station_name = request.POST['spec_station']
            reporter_location = request.POST['reporter_location']
            spec_locs = SpecLoc.objects.filter(enforcement_loc=spec_station_name)
            for i in spec_locs:
                if i.reporter_loc==reporter_location:
                    instance.spec_location = i
            instance.save()
            public_report = form.save()
            fir_id = public_report.id
            template_path = 'public_template.html'  # Path to your PDF template
            context = {'public_report': public_report, 'fir_id': fir_id}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Report_{fir_id}.pdf"'

            template = get_template(template_path)
            html = template.render(context)

            # Create PDF document
            pdf_response = pisa.CreatePDF(html, dest=response)

            if not pdf_response.err:
                return response
            return redirect('/')
    else:
        form = CrimeReportForm()
        
    print(form.errors)
    messages.error(request, form.errors)
    
    return render(request, 'report_public.html', {'form': form, 'location_options':location_options})

@login_required
def listcrime(request):
    user_crime=request.user
    list_dict=CrimeReport.objects.filter(list_user=user_crime)
    return render(request, 'listcrime.html', {'list_dict': list_dict})

def law_index(request):
    return render(request,'law_index.html')

def law_login(request):
    return render(request,'law_login.html')

# def law_update_status(request, crime_id):
#     if request.method == 'POST':
#         new_status = request.POST.get('status')
#         crime_report = CrimeReport.objects.get(pk=crime_id)
#         crime_report.status = new_status
#         crime_report.save()
#         return redirect('list_crimes')

def law_update_status(request):
    crime_reports = CrimeReport.objects.all()
    return render(request, 'law_update_status.html', {'crime_reports': crime_reports})
    

def update_status(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_status = request.POST.get('status')
        try:
            # Update the status in the database
            report = CrimeReport.objects.get(pk=report_id)
            report.status = new_status
            report.save()
            return redirect('law_update_status') 
        except CrimeReport.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Report not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# def update_crime_status(request):
#     if request.method == 'POST':
#         crime_id = request.POST.get('crime_id')
#         status = request.POST.get('status')

#         # Update the status in your database for the specified crime_id
#         try:
#             crime = CrimeReport.objects.get(pk=crime_id)
#             crime.status = status
#             crime.save()
#             return JsonResponse({'success': True})
#         except CrimeReport.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Crime report not found'})

#     return JsonResponse({'success': False, 'error': 'Invalid request method'})

def check_reporter_loc(request):
    if request.method == 'GET':
        reporter_loc = request.GET.get('reporter_loc', None)
        if reporter_loc:
            try:
                # Assuming you have a SpecLoc model
                spec_location = SpecLoc.objects.get(reporter_loc=reporter_loc)
                data = {'valid': True, 'enforcement_loc': spec_location.enforcement_loc}
            except SpecLoc.DoesNotExist:
                data = {'valid': False}
        else:
            data = {'valid': False}
        return JsonResponse(data)
    else:
        return JsonResponse({'valid': False})
    
def crime_category(request):
    return render(request,'crimecategory.html')

def view_crime(request,crime_id):
    task=CrimeReport.objects.get(id=crime_id)
    form=CrimeReportForm(request.POST or None,instance=task)
    return render(request,'view_crime.html',{'form':form})

from django.http import JsonResponse

def upload_evidence(request):
    if request.method == 'POST' and request.FILES.get('evidence_pic_vid_aud'):
        uploaded_file = request.FILES['evidence_pic_vid_aud']

        # Ensure that the CrimeReport with the given ID exists
        crime_report_id = request.POST.get('crime_report_id')
        try:
            crime_report = CrimeReport.objects.get(id=crime_report_id)
        except CrimeReport.DoesNotExist:
            return JsonResponse({'message': 'CrimeReport does not exist'}, status=400)

        fir_file = FIRFile(crime_report=crime_report, file=uploaded_file)
        fir_file.save()

        return JsonResponse({'message': 'File uploaded successfully'})

    return JsonResponse({'message': 'File upload failed'}, status=400)
