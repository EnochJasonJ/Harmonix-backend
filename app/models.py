from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberModel(models.Model):
    DEPT_CHOICES = [
        ('CSE',"Computer Science Engineering"),
        ('AIML',"Artificial Intelligence and Machine Learning"),
        ('AIDS',"Artificial Intelligence and Data Science"),
        ('CSBS',"Computer Science and Business Systems"),
        ('ECE',"Electronics and Communication Engineering"),
        ('EEE',"Electrical and Electronics Engineering"),
        ('CCE',"Computer and Communication Engineering"),
        ('MECH',"Mechanical Engineering"),
        ('IT',"Information Technology"),
    ]
    YEAR_CHOICES = [
        ('I', 'First Year'),
        ('II', 'Second Year'),
        ('III', 'Third Year'),
        ('IV', 'Fourth Year'),
    ]
    CLUB_CHOICES = [
        ('Harmonix', 'Harmonix'),
        ('Groovex', 'Groovex'),
    ]
    
    POSITION_CHOICES = [
        ('Member', 'Member'),
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Joint-Secretary', 'Joint-Secretary'),
    ]
    ROLE_CHOICES = [
        ('Vocalist', 'Vocalist'),
        ('Guitarist', 'Guitarist'),
        ('Drummer', 'Drummer'),
        ('Keyboardist', 'Keyboardist'),
        ('Bassist', 'Bassist'),
        ('Dancer', 'Dancer')
    ]
    USER_ROLE = [
        ('Admin', 'Admin'),
        ('User', 'User')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=4, choices=DEPT_CHOICES, default='CSE')
    year = models.CharField(max_length=4, choices= YEAR_CHOICES, default='I')
    club = models.CharField(max_length=100,choices=CLUB_CHOICES , default='Harmonix')
    role = models.CharField(max_length=100,choices=ROLE_CHOICES ,default='Vocalist')
    position = models.CharField(max_length=100,choices=POSITION_CHOICES ,default='Member')
    user_role = models.CharField(max_length=100, choices=USER_ROLE, default='User')
    event_counts = models.IntegerField(default=0)
    present_days = models.IntegerField(default=0, null=True, blank=True)
        
    def __str__(self):
        return self.user.username
    
    @property
    def present_days_count(self):
        return self.attendancemodel_set.filter(is_present=True).count()
        # return self.present_days if self.present_days is not None else 0
    
    # @property
    def update_present_days(self):
        self.present_days = self.attendancemodel_set.filter(is_present=True).count()
        self.save()
    
class AttendanceModel(models.Model):
    
    member = models.ForeignKey(MemberModel, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    club = models.CharField(max_length=100,choices=MemberModel.CLUB_CHOICES ,default='Harmonix')
    
    class Meta:
        unique_together = ('member', 'date')
        
    def __str__(self):
        return f"{self.member.user.username} - {self.date} - {'Present' if self.is_present else 'Absent'}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.member:
            self.member.present_days = self.member.attendancemodel_set.filter(is_present=True).count()
            self.member.save()
    
class EventModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    club = models.CharField(max_length=100, choices=MemberModel.CLUB_CHOICES, default='Harmonix')
    members_participated = models.ManyToManyField(MemberModel, related_name='events_participated', blank=True)
    
    def __str__(self):
        return self.name