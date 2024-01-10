from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
#from .models import User
from .forms import CrimeReportForm, AnonyReportForm, DocReportForm, PublicForm, PublicForm, EvidenceCrimeForm, PrisonReportForm
from .models import CustomUser, CrimeReport, DocReport, Jailor, SpecLoc, FIRFile, PublicReport, EvidenceCrimeReport, PrisonReport, Inmate
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
from django.http import JsonResponse, FileResponse
from django.template.loader import get_template
from django.urls import reverse
from django.http import Http404
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == 'POST':
        # Retrieve form data from request.POST
        your_name = request.POST.get('your_name', '')
        phone_number = request.POST.get('phone_number', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        # Handle the form data as needed
        print(f"Name: {your_name}, Phone Number: {phone_number}, Email: {email}, Message: {message}")

        # Send email
        subject = 'Contact Us Form Submission'
        message_body = f"Name: {your_name}\nPhone Number: {phone_number}\nEmail: {email}\nMessage: {message}"
        from_email = {email}  # Replace with your email address
        recipient_list = ['reportsafer@gmail.com']
        send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

        messages.warning(request, "Your Response Sent!!")
        # return HttpResponse("Form submitted successfully and email sent!")

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
                'reportsafer@gmail.com',
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
                if user.is_prison:
                    return redirect('prisonstaff')
                if user.is_control:
                    return redirect('control')
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
            response['Content-Disposition'] = f'inline; filename="Report_{fir_id}.pdf"'

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

def law_page(request):
    crime_reports = CrimeReport.objects.all()
    doc_reports = DocReport.objects.all()
    public_reports = PublicReport.objects.all()
    # Assuming you have models associated with the forms
    data1 = CrimeReport.objects.all()
    data2 = DocReport.objects.all()
    data3 = PublicReport.objects.all()
    return render(request,'law_page.html', {
            'crime_reports': crime_reports,
            'doc_reports': doc_reports,
            'public_reports': public_reports,
            'data_from_model1': data1,
            'data_from_model2': data2,
            'data_from_model3': data3,
        })

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
        form = DocReportForm(request.POST,request.FILES)
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

    # if request.method == 'POST':
    #     # Process the form submission
    #     form = DocReportForm(request.POST, request.FILES)  # Use your form if you have one
    #     if form.is_valid():
    #         # Create a new DocumentReport object and save it to the database
    #         report = form.save(commit=False)
    #         report.user = request.user  # Assuming you have a user associated with the report
    #         report.save()
            

    #         # Define the context for your template
    #         context = {'report': report}
    #         messages.success(request, 'Your report has been submitted successfully.')
    #         return redirect('index')  # Redirect to the desired page after successful submission
    #     else:
    #         messages.error(request, form.errors)
    # else:
    #     # Render the initial form
    #     form = DocReportForm() 
    # return render(request, 'report_doc.html', {'form': form})


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
            response['Content-Disposition'] = f'inline; filename="FIR_{fir_id}.pdf"'  # Use f-string to include fir_id

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
            response['Content-Disposition'] = f'inline; filename="Report_{fir_id}.pdf"'

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
    crime_dict=CrimeReport.objects.filter(list_user=user_crime)
    doc_dict=DocReport.objects.filter(list_user=user_crime)
    public_dict=PublicReport.objects.filter(list_user=user_crime)
    combined_reports = list(crime_dict) + list(doc_dict) +list(public_dict)
    return render(request, 'listcrime.html', {'combined_reports': combined_reports})

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
    doc_reports = DocReport.objects.all()
    public_reports = PublicReport.objects.all()
    # Assuming you have models associated with the forms
    data1 = CrimeReport.objects.all()
    data2 = DocReport.objects.all()
    data3 = PublicReport.objects.all()
    return render(request,'law_update_status.html', {
            'crime_reports': crime_reports,
            'doc_reports': doc_reports,
            'public_reports': public_reports,
            'data_from_model1': data1,
            'data_from_model2': data2,
            'data_from_model3': data3,
        })

def update_status(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        doc_id = request.POST.get('doc_id')
        public_id = request.POST.get('public_id')
        new_status = request.POST.get('status')
        if report_id:
            report = CrimeReport.objects.get(pk=report_id)
            report.status = new_status
            report.save()
            
            # Redirect to the view_crime page for CrimeReport with the updated status
            return redirect('view_crime', crime_id=report_id)
            
        elif doc_id:
            report_ = DocReport.objects.get(pk=doc_id)
            report_.status = new_status
            report_.save()
            
            # Redirect to the view_crime page for DocReport with the updated status
            return redirect('view_crime', crime_id=doc_id)
            
        elif public_id:
            report_p = PublicReport.objects.get(pk=public_id)
            report_p.status = new_status
            report_p.save()
            
            # Redirect to the view_crime page for PublicReport with the updated status
            return redirect('view_crime', crime_id=public_id)
    
    # Handle invalid request method here
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

def control(request):
    return render(request,'control.html')

def view_crime(request, crime_id):
    try:
        task = CrimeReport.objects.get(id=crime_id)
        form = CrimeReportForm(request.POST or None, instance=task)
        try:
            evidence = EvidenceCrimeReport.objects.get(crime_idnum_id=crime_id)
            file_evidence = EvidenceCrimeForm(request.POST or None, instance=evidence)
            return render(request, 'view_crime.html', {'form': form, 'form_id': crime_id, 'form_status': task.status, 'file_evidence': file_evidence})
        except EvidenceCrimeReport.DoesNotExist:
            return render(request, 'view_crime.html', {'form': form, 'form_id': crime_id, 'form_status': task.status, 'file_evidence': None})
    except CrimeReport.DoesNotExist:
        task = DocReport.objects.get(id=crime_id)
        form = DocReportForm(request.POST or None, instance=task)
        return render(request, 'view_crime.html', {'form': form, 'form_id': crime_id})
 
# def up_final(request):
#     if request.method == 'POST':
#         # Create a new instance of CrimeReport and save it
#         crime_report_form = EvidenceCrimeForm(request.POST)
#         if crime_report_form.is_valid():
#             crime_report = crime_report_form.save()

#             # Get the uploaded "Final Report" file and store it in document_final field
#             final_report_file = request.FILES.get('evidence_final')
#             if final_report_file:
#                 evidence_report = EvidenceCrimeReport(
#                     crime_idnum=crime_report,
#                     document_final=final_report_file,
#                 )
#                 evidence_report.save()

#             return redirect('success_url')  # Replace 'success_url' with your desired URL

#     # Handle GET request or form validation errors
#     else:
#         crime_report_form = EvidenceCrimeForm()

#     return render(request, 'view_crime.html', {'crime_report_form': crime_report_form})
def up_final(request):
    if request.method == 'POST':
        crime = request.POST.get('crime_idnum')

        if crime is not None:
            try:
                crime_report = CrimeReport.objects.get(id=int(crime))
            except (CrimeReport.DoesNotExist, ValueError):
                crime_report = None  # Handle the case where the CrimeReport doesn't exist or the ID is not valid
        else:
            crime_report = None
        if crime_report:
            try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
            except EvidenceCrimeReport.DoesNotExist:
                evidence = None

            form = EvidenceCrimeForm(request.POST, request.FILES, instance=evidence)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.crime_idnum = crime_report
                instance.save()
                return redirect(reverse('view_crime', kwargs={'crime_id': crime_report.id}))  # Corrected this line
        else:
            return redirect('/')
    else:
        form = EvidenceCrimeForm()
    
    # You should pass the crime_report ID here; this line assumes you have the ID from somewhere
    return redirect(reverse('view_crime', kwargs={'crime_id': crime_report.id, 'form': form}))

from django.shortcuts import render, redirect
from .models import CrimeReport, EvidenceCrimeReport
from .forms import EvidenceCrimeForm

def fir(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid
        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.status = 'Preliminary Investigation completed'
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})

def witness(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.witness()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})

def forensic(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.forensic()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})
def arrest(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.arrest()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})
def charge(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.charge()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})
def case(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.case()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})
def final(request):
    if request.method == 'POST':
        crime_id = request.POST.get('crime_idnum')
        crime_report = CrimeReport.objects.get(id=crime_id)  # Assuming the crime_id is valid

        try:
                evidence = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
        except EvidenceCrimeReport.DoesNotExist:
                evidence = None
        # Create an instance of the EvidenceCrimeForm
        form = EvidenceCrimeForm(request.POST, request.FILES,instance=evidence)

        if form.is_valid():
            # Save the form data without committing to the database
            instance = form.save(commit=False)
            instance.crime_idnum = crime_report  # Associate the evidence with the crime report
            instance.save()  # Commit to the database

            # Update the status of the crime report to 'Preliminary Investigation completed'
            crime_report.final()
            crime_report.save()

            return redirect('view_crime', crime_id=crime_id)
    else:
        form = EvidenceCrimeForm()

    return render(request, 'view.html', {'form': form})
# Import your models and forms here


# def up_final(request):
#     if request.method == 'POST':
#         form = EvidenceCrimeForm(request.POST, request.FILES)
#         crime_id = request.POST.get('crime_idnum')
        
#         try:
#             crime_report = CrimeReport.objects.get(id=int(crime_id))
#         except (CrimeReport.DoesNotExist, ValueError):
#             crime_report = None  # Handle the case where the CrimeReport doesn't exist or the ID is not valid
        
#         if crime_report:
#             # Try to get an existing EvidenceCrimeReport object for the given crime_id
#             try:
#                 evidence_report = EvidenceCrimeReport.objects.get(crime_idnum=crime_report)
#                 # Update the existing object's fields with the form data
#                 form = EvidenceCrimeForm(request.POST, request.FILES, instance=evidence_report)
#             except EvidenceCrimeReport.DoesNotExist:
#                 evidence_report = None  # Handle the case where the EvidenceCrimeReport doesn't exist

#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.crime_idnum = crime_report
#                 instance.save()
#                 return redirect(reverse('view_crime', kwargs={'crime_id': crime_report.id}))
            
    #     else:
    #         # Handle the case where the CrimeReport doesn't exist or the ID is not valid
    #         raise Http404("CrimeReport not found")

    # else:
    #     form = EvidenceCrimeForm()
    # return render(request, 'view_crime.html', {'form': form})

def view_doc(request,crime_id):
    try:
        task=DocReport.objects.get(id=crime_id)
        form=DocReportForm(request.POST or None,instance=task)
        return render(request,'view_doc.html',{'form':form})
    except DocReport.DoesNotExist:
        task=DocReport.objects.get(id=crime_id)
        form=DocReportForm(request.POST or None,instance=task)
        return render(request,'view_doc.html',{'form':form})
    
def view_public(request,crime_id):
    try:
        task=PublicReport.objects.get(id=crime_id)
        form=PublicForm(request.POST or None,instance=task)
        return render(request,'view_public.html',{'form':form})
    except PublicReport.DoesNotExist:
        task=PublicReport.objects.get(id=crime_id)
        form=PublicForm(request.POST or None,instance=task)
        return render(request,'view_public.html',{'form':form})

def upload_evidence(request):
    if request.method == 'POST' and request.FILES.get('evidence_image_label'):
        uploaded_file = request.FILES['evidence_image_label']

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

def prisonstaff(request):
    return render(request,'prisonstaff.html')

def control_page(request):
    crime_reports = CrimeReport.objects.all()
    doc_reports = DocReport.objects.all()
    public_reports = PublicReport.objects.all()
    # Assuming you have models associated with the forms
    data1 = CrimeReport.objects.all()
    data2 = DocReport.objects.all()
    data3 = PublicReport.objects.all()
    return render(request,'control_page.html', {
            'crime_reports': crime_reports,
            'doc_reports': doc_reports,
            'public_reports': public_reports,
            'data_from_model1': data1,
            'data_from_model2': data2,
            'data_from_model3': data3,
        })

def control_status(request):
    crime_reports = CrimeReport.objects.all()
    doc_reports = DocReport.objects.all()
    public_reports = PublicReport.objects.all()
    # Assuming you have models associated with the forms
    data1 = CrimeReport.objects.all()
    data2 = DocReport.objects.all()
    data3 = PublicReport.objects.all()
    return render(request,'control_status.html', {
            'crime_reports': crime_reports,
            'doc_reports': doc_reports,
            'public_reports': public_reports,
            'data_from_model1': data1,
            'data_from_model2': data2,
            'data_from_model3': data3,
        })

def report_prison(request):
    form = PrisonReportForm(request.POST)
    
    pri = form.save(commit=False)
    print(form.errors)
        # Set the organizer to the currently logged-in user
    pri.org_user = request.user
    pri.save()  # Commit the webinar to the database

        # Process speakers
    inmate_name = request.POST.getlist('inmate_name[]')
    inmate_id = request.POST.getlist('inmate_id[]')
    for i in range(len(inmate_name)):
        inmate = Inmate.objects.create(
            inmate_name = inmate_name[i],
            inmate_id = inmate_id[i]
        )
        pri.inmates.add(inmate)
    return render(request,'report_prison.html')

from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages




def book_appointment(request):
    inmates = Inmate.objects.all()
    if request.method == 'POST':
        in_id = request.POST.get('in_name')
        time = request.POST.get('timet')
        date = request.POST.get('dated')
        # Check if the selected time slot is available and other validation if needed
        # If the time slot is available, create an Appointment instance and save it
        appointment = Appointment(ap_name=in_id, time_slot=time, date=date)
        print(appointment)
        appointment.save()

        # You can also add additional logic, such as sending confirmation emails

        # Add a success message
        messages.success(request, 'Appointment booked successfully.')

        return redirect('book_appointment')  # Redirect to the same page or another page
    else:
        # Handle GET requests if needed
        return render(request, 'book_appointment.html',{'inmates': inmates})
    
    
def appointment_view(request):
    appointments = Appointment.objects.all()  # Retrieve all appointments
    return render(request, 'view_appointment.html', {'appointments': appointments})

def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(phone_number, otp):
    phone_number_with_country_code = '+91' + phone_number
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        message = client.messages.create(
            to=phone_number_with_country_code,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=f'Your OTP is: {otp}'
        )
        print(message.sid) 
    except Exception as e:
        print(f"Error sending OTP: {e}")

def login_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        if not phone_number:
            messages.error(request, 'Phone number is required.')
            return render(request, 'login/login_via_otp.html')

        phone_number = phone_number.replace(" ", "")
        if len(phone_number) != 10 or not phone_number.isdigit():
            messages.error(request, 'Invalid phone number.')
            return render(request, 'login/login_via_otp.html')

        # Generate and send OTP
        otp = generate_otp()
        send_otp(phone_number, otp)

        # Save OTP and phone number in session for verification
        request.session['login_otp'] = otp
        request.session['login_phone'] = phone_number

        return redirect('otp_verification')  # Redirect to the OTP verification page

    return render(request, 'login/login_via_otp.html')

def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('entered_otp')
        stored_otp = request.session.get('login_otp')
        phone_number = request.session.get('login_phone')
        
        print(f"Entered OTP: {entered_otp}")
        print(f"Stored OTP: {stored_otp}")
        print(f"Phone Number: {phone_number}")

        if entered_otp == stored_otp:
            print("Entered authentication")
            User = get_user_model()
            user = authenticate(request, phone=phone_number)  # No need to provide a password

            if user:
                login(request, user)
                print("User authenticated and logged in:", user)
                
                if user.user_type == 'admin':
                    return redirect(reverse('admin_dashboard'))
                elif user.user_type == 'client':
                    return redirect(reverse('client_dashboard'))
                elif user.user_type == 'lawyer':
                    # Assuming you have a one-to-one relationship between CustomUser and LawyerProfile
                    lawyer_profile = LawyerProfile.objects.get(user=user)
                    if lawyer_profile.time_update is None or (timezone.now() - lawyer_profile.time_update).days > 14:
                        return redirect(reverse('assign_working_hours'))
                    else:
                        return redirect(reverse('lawyer_dashboard'))
                elif user.user_type == 'student':
                    return redirect(reverse('student_dashboard'))
            else:
                messages.error(request, 'Invalid OTP. Please try again')

    return render(request, 'login/otp_verification.html')