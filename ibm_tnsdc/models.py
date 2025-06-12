from django.db import models

# Create your models here.
class College(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.TextField(null=True,blank=True)
    team_size = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.college_name

    class Meta(object):
        verbose_name = 'Colleges'
        verbose_name_plural = 'Colleges'

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.TextField(null=True,blank=True)
    project_description = models.TextField(null=True,blank=True)
    course_id = models.CharField(max_length=255,null=True,blank=True)
    course_name = models.TextField(null=True,blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.project_name

    class Meta(object):
        verbose_name = 'Projects'
        verbose_name_plural = 'Projects'

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    role = models.CharField(max_length=255,null=True,blank=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE,null=True,blank=True)
    course_id=models.TextField(null=True,blank=True)

    def __str__(self):
        # return (self.first_name or "") + " "+ (self.last_name or "")
        return self.email

    class Meta(object):
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    team_name = models.TextField(null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.team_name

    class Meta(object):
        verbose_name = 'Teams'
        verbose_name_plural = 'Teams'


class TeamMembers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True,blank=True)

    @property
    def project(self): # this is the property method
        return self.team.project # this returns the project attribute of the related Team object

    def __str__(self):
        return "__all__"

    class Meta(object):
        verbose_name = 'TeamMembers'
        verbose_name_plural = 'TeamMembers'

        
