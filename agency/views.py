from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Service, TeamMember, ContactInquiry

def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]
    all_services = Service.objects.all()
    return render(request, 'agency/home.html', {
        'featured_projects': featured_projects,
        'services': all_services,
    })

def work_list(request):
    # Ambil semua project, urutkan dari yang terbaru
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'agency/work.html', {'projects': projects})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'agency/work_detail.html', {'project': project})


# View untuk menampilkan DETAIL SERVICE (berisi fitur-fitur)
def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'agency/expertise_detail.html', {'service': service})

# View untuk menampilkan DAFTAR SEMUA SERVICE (opsional)
def expertise_list(request):
    services = Service.objects.all()
    return render(request, 'agency/expertise_list.html', {'services': services})

def about(request):
    # Ambil data team member
    team_members = TeamMember.objects.all()
    return render(request, 'agency/about.html', {'team_members': team_members})

def contact(request):
    message_sent = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')
        
        # Simpan ke database
        if name and email and message_content:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                message=message_content
            )
            message_sent = True
    
    return render(request, 'agency/contact.html', {'message_sent': message_sent})

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)