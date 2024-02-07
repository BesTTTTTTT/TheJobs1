from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job
from fuzzywuzzy import fuzz
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

def home(request):
    return render(request,'base.html')
def homes(request):
    return render(request, 'base1.html')

def forms_view(request):
    return render(request, 'forms.html', {})


def apply_custom(request):
    if request.method == "POST":
        table = custom()
        table.custom_name = request.POST['custom_name']
        table.custom_lastname = request.POST['custom_lastname']
        table.email = request.POST['email']
        table.address = request.POST['address']
        table.province = request.POST['province']
        table.zip = request.POST['zip']
        table.gender = request.POST['gender']
        company_name = request.POST['company']
        position_applied = request.POST['position_applied']
        company = Company.objects.get(company_name=company_name)
        table.company = company
        table.position_applied = position_applied
        table.status = 'เรียบร้อย' 
        table.source = request.POST.get('source', '')
        table.tal_phon = request.POST['tal_phon']
        table.cv_file = request.FILES.get('cv_file', None)  
        table.save()
        messages.success(request, 'สมัครงานเสร็จสิ้น')
        return redirect('/search')  

    return render(request, 'forms.html')


def add_jobcompany(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        Typework = request.POST.get('Typework')
        salary = request.POST.get('salary')

       
        if title and description and location and Typework and salary:
       
            job = Job.objects.create(
                title=title,
                description=description,
                location=location,
                Typework=Typework,
                salary=salary,
                company=request.user.employee.company
            )
            return redirect('company_jobs')

    return render(request, 'add_jobcompany.html')

@login_required(login_url="/login")
def edit_jobs(request):
    return render(request, 'edit_job.html')

@login_required(login_url="/login")
def edit_form(request, pk=None):
    context = {}
    if pk is not None:
        job_instance = get_object_or_404(Job, pk=pk)
        context["job"] = job_instance
        if request.method == "POST":
            job_instance.title = request.POST.get('title')
            job_instance.description = request.POST.get('description')
            job_instance.location = request.POST.get('location')
            job_instance.time = request.POST.get('time')
            job_instance.salary = request.POST.get('salary')
            messages.success(request, 'เเก้ไขงานเสร็จสิ้น')
            job_instance.save()
    return render(request, 'edit_view.html', context)


from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
def login_company(request):
    companies = Company.objects.all()  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_id = request.POST.get('company')  
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                employee = user.employee 
                if employee.company.id == int(company_id):
                    login(request, user)
                    return redirect('/base1')
                else:
                    messages.error(request, 'ผู้ใช้ไม่เกี่ยวข้องกับบริษัทที่เลือก.')
            except ObjectDoesNotExist:
                messages.error(request, 'ผู้ใช้ไม่มีพนักงานที่เกี่ยวข้อง.')
        else:
            messages.error(request, 'รหัสไม่ถูกต้องประจำตัวที่ไม่ถูกต้อง!')

    return render(request, 'company_login.html', {'companies': companies})

def company_jobs(request):
   
    company_jobs = Job.objects.filter(company=request.user.employee.company)
    
    context = {'company_jobs': company_jobs}
    return render(request, 'company_jobs.html', context)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'เข้าสู่ระบบสําเร็จ')
            return redirect('/')
        else:
            messages.error(request, 'รหัสไม่ถูกต้อง !')
            pass
    return render(request, 'login.html')




def logout_view(request):
        logout(request)
        return redirect('/login')

def register_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        company_name = request.POST.get('company_name')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'รหัสนี้มีคนใช้เเล้ว!')
        else:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            company, created = Company.objects.get_or_create(company_name=company_name)
            employee = Employee.objects.create(user=new_user, company=company)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/company_login')
            else:
                messages.error(request, 'Login failed')

    return render(request, 'register_company.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'รหัสนี้มีคนใช้เเล้ว !')
        else:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            return redirect('/login')

    return render(request, 'register.html')


def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'search_jobs.html', {'jobs': jobs})

from django.db.models import Count
@login_required(login_url="/login")
def job_search(request):
    query = request.GET.get('q', '')
    company = request.GET.get('company', '')
    location = request.GET.get('location', '')
    typework = request.GET.get('Typework', '')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |  
            Q(description__icontains=query) |
            Q(company__company_name__icontains=query) | 
            Q(Typework__icontains=query) |  
            Q(location__icontains=query)
        )

    if company:
        jobs = jobs.filter(company__company_name__icontains=company)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if typework:
        jobs = jobs.filter(Typework__icontains=typework)

    paginator = Paginator(jobs, 4)  
    page = request.GET.get('page')

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)

    companies = Job.objects.values('company__company_name').annotate(total=Count('company')).order_by('company__company_name')
    locations = Job.objects.values('location').annotate(total=Count('location')).order_by('location')
    typeworks = Job.objects.values('Typework').annotate(total=Count('Typework')).order_by('Typework')

    return render(request, 'search.html', {'jobs': jobs, 'query': query, 'company': company, 'location': location, 'companies': companies, 'locations': locations, 'typework': typework, 'typeworks': typeworks})




def search_jobs(query, company=None, location=None, typework=None):
    queryset = Job.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |  
            Q(description__icontains=query) |
            Q(company__company_name__icontains=query) |  # ปรับให้ใช้ company_name
            Q(Typework__icontains=query) |
            Q(location__icontains=query)
        )
    if company:
        queryset = queryset.filter(company__company_name__icontains=company)  # ปรับให้ใช้ company_name
    if location:
        queryset = queryset.filter(location__icontains=location)
    if typework:
        queryset = queryset.filter(Typework__icontains=typework)
    return queryset






@login_required(login_url="/login")
def job_searchadmin(request):
    query = request.GET.get('q', '')
    company = request.GET.get('company', '')
    location = request.GET.get('location', '')
    typework = request.GET.get('Typework', '')
    if company and location and typework:
        jobs = search_jobsadmin(query, company=company, location=location , typework=typework)
    elif company:
        jobs = search_jobsadmin(query, company=company)
    elif location:
        jobs = search_jobsadmin(query, location=location)
    elif typework:
        jobs = search_jobsadmin(query, typework=typework)
    else:
        jobs = search_jobsadmin(query)
    paginator = Paginator(jobs, 4)  
    page = request.GET.get('page')

    try:
        jobs = paginator.page(page)
    except PageNotAnInteger:
      
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    companies = Job.objects.values_list('company', flat=True).distinct()    
    locations = Job.objects.values_list('location', flat=True).distinct()
    typeworks = Job.objects.values_list('Typework', flat=True).distinct()
    return render(request, 'edit_job.html', {'jobs': jobs, 'query': query, 'company': company, 'location': location, 'companies': companies, 'locations': locations,'typework': typework, 'typeworks': typeworks})


def search_jobsadmin(query, company=None, location=None, typework=None):
    queryset = Job.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(Typework__icontains=query)
        )
    if company:
        queryset = queryset.filter(company__icontains=company)
    if location:
        queryset = queryset.filter(location__icontains=location)
    if typework:
        queryset = queryset.filter(Typework__icontains=typework)
    return queryset


def edit_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'edit_view.html', {'job': job})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_detail.html', {'job': job})


def cst_detail(request, pk):
    custom_instance = get_object_or_404(custom, pk=pk)
    context = {
        'custom_instance': custom_instance,
    }
    return render(request, 'cst_detail.html', context)



from django.core.mail import send_mail
from django.conf import settings

def send_emails(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name', '')  
        email = request.POST.get('email', '')  
        message = request.POST.get('message', '')  
        approval = request.POST.get('approval', '')

        subject = f'จากบริษัท - {company_name}'
        email_message = f'การอนุมัติ: {approval}\nข้อความข้างต้น: {message}'
        send_mail(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        messages.success(request, 'ส่งอีเมลเรียบร้อย')
        return render(request, 'send_email_form.html')

def send_email_form(request, email):
 
    return render(request, 'send_email_form.html', {'email': email})





def your_forms_view_name(request, title, company):
    job = Job.objects.get(title=title, company__company_name=company)
    return render(request, 'forms.html', {'job': job})




def custom_lists(request):

    try:
        employee = Employee.objects.get(user=request.user)
        company = employee.company
    except Employee.DoesNotExist:
     
        return HttpResponse("/")

    custom_objects = custom.objects.filter(company=company)
    return render(request, 'custom_list.html', {'custom_objects': custom_objects})



def custom_objects_list(request):
    custom_objects = custom.objects.all()
    return render(request, 'custom_lists.html', {'custom_objects': custom_objects})




def add_jobs(request):
    if request.method == "POST":
        table = Job()
        table.title = request.POST['title']
        table.description = request.POST['description']
        table.company = request.POST['company']
        table.location = request.POST['location']
        table.time = request.POST['time']
        table.Typework = request.POST['Typework']
        table.salary = request.POST['salary']
        table.save()
        messages.success(request, 'เพิ่มงานเสร็จสิ้น')
    return render(request,'add_job.html')




def manage_drug(request):
    show_drug = custom.objects.all()
    context  = {"custom" : show_drug}
    return render(request,'edit_drug.html',context)

def delete_custom(request, custom_id):

    custom_instance = get_object_or_404(custom, pk=custom_id)

    custom_instance.delete()
    return redirect('/custom_list')

 
 
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, pk=job_id)
        job.delete()
        messages.success(request, 'ลบงานเสร็จสิ้น')
        return redirect('company_jobs')  
    else:
        return redirect('company_jobs') 