from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import URLValidator


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('mobile', 'Mobile'),
        ('database', 'Database'),
        ('tools', 'Tools & DevOps'),
        ('testing', 'Testing & QA'),
        ('soft', 'Soft Skills'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.IntegerField(default=50, help_text="0-100")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        ordering = ['category', 'order', 'name']


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Education"


class Project(models.Model):
    PROJECT_STATUS = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]

    PROJECT_TYPE = [
        ('freelance', 'Freelance'),
        ('personal', 'Personal'),
        ('academic', 'Academic'),
        ('open_source', 'Open Source'),
    ]

    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=250)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='completed')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    technologies = models.CharField(max_length=500, help_text="Comma-separated tech stack")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',')]

    class Meta:
        ordering = ['-featured', 'order', '-created_at']


class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    technologies = models.CharField(max_length=500, blank=True, help_text="Comma-separated")
    achievements = models.TextField(blank=True, help_text="One achievement per line")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.position} at {self.company}"

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def get_achievements_list(self):
        return [ach.strip() for ach in self.achievements.split('\n') if ach.strip()]

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Experience"


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.issuer}"

    class Meta:
        ordering = ['-issue_date']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated")
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    class Meta:
        ordering = ['-created_at']