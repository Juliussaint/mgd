from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="Font Awesome class (e.g., fa-solid fa-pen-nib)")
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title
    
class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.service.title} - {self.title}"

class ProjectCategory(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    client_name = models.CharField(max_length=100, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='projects/thumbnails/')
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text="e.g. React, Three.js")
    project_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False, help_text="Show on homepage?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/') # Folder terpisah dari thumbnail
    order = models.IntegerField(default=0) # Untuk mengurutkan gambar

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/')
    
    def __str__(self):
        return f"{self.name} - {self.role}"

class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inquiry from {self.email}"