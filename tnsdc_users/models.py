from django.db import models
from django.contrib.auth.models import User
# from opaque_keys.edx.django.models import CourseKeyField

class Colleges(models.Model):
    id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=100, blank=True, verbose_name='College Names')
    college_code = models.CharField(max_length=100, blank=True, verbose_name='College Code')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Colleges')
        verbose_name_plural = ('Colleges')
    def __str__(self):
        return self.college_name
class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    session_name = models.CharField(max_length=100, blank=True, verbose_name='Session Names')
    batch = models.CharField(max_length=100, blank=True, verbose_name='Batches')
    year = models.CharField(max_length=100, blank=True, verbose_name='Year')
    start_date = models.DateTimeField(null=True) 
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False, verbose_name='Is Active')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Session')
        verbose_name_plural = ('Sessions')
    def __str__(self):
        return self.session_name
class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=100, blank=True, verbose_name='Branch Names')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Branch')
        verbose_name_plural = ('Branches')
    def __str__(self):
        return self.branch_name
class Technologies(models.Model):
    id = models.AutoField(primary_key=True)
    tech_name = models.CharField(max_length=100, blank=True, verbose_name='Tech Names')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Technology')
        verbose_name_plural = ('Technologies')
    def __str__(self):
        return self.tech_name
class BranchTechnology(models.Model):
    id = models.AutoField(primary_key=True)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True)
    tech_id = models.ForeignKey(Technologies, on_delete=models.CASCADE, blank=True, null=True)
    sessions_id = models.ForeignKey(Sessions, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Branch Technology')
        verbose_name_plural = ('Branch Technologies')
    def __str__(self):
        return "{0} - {1} {2}".format(self.id, self.branch_id, self.tech_id)
class Groups(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=100, blank=True, verbose_name='Group Names')
    sessions_id = models.ForeignKey(Sessions, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Group')
        verbose_name_plural = ('Groups')
    def __str__(self):
        return self.group_name
class CollegeGroupSession(models.Model):
    id = models.AutoField(primary_key=True)
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE, blank=True, null=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, blank=True, null=True)
    sessions_id = models.ForeignKey(Sessions, on_delete=models.CASCADE, blank=True, null=True)
    projected_student_count = models.IntegerField(default=0)
    team_size = models.IntegerField(default=0)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('College Group Session')
        verbose_name_plural = ('College Group Sessions')
    def __str__(self):
        return "{0} - {1} {2}".format(self.id, self.college_id, self.group_id)
    
class CourseMappings(models.Model):
    id = models.AutoField(primary_key=True)
    # sko_course_id = CourseKeyField(max_length=255, db_index=True)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE, blank=True, null=True)
    tech_id = models.ForeignKey(Technologies, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Course Mappings')
        verbose_name_plural = ('Course Mappings')
class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    # course_id = CourseKeyField(max_length=255, db_index=True)
    project_name = models.CharField(max_length=100, blank=True, verbose_name='Project Names')
    project_description = models.CharField(max_length=100, blank=True, verbose_name='Project Descriptions')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Projects')
        verbose_name_plural = ('Projects')
    def __str__(self):
        return self.project_name
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_names = models.CharField(max_length=100, blank=True, verbose_name='Role Names')
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Roles')
        verbose_name_plural = ('Roles')
    def __str__(self):
        return self.role_names
class UserRoles(models.Model):
    id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='user_role')
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('User Roles')
        verbose_name_plural = ('User Roles')
    def __str__(self):
        return "{0} - {1} {2}".format(self.id, self.role_id, self.user_id)

class UserBranch(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,related_name='user_branch')
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('User Branch')
        verbose_name_plural = ('User Branches')
    
class StudentDetails(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='std_details')
    nm_id = models.CharField(max_length=100, blank=True, verbose_name='nm_id')
    anna_univ_id = models.CharField(max_length=100, blank=True, verbose_name='anna_univ_id')    
    college_id = models.ForeignKey(Colleges, on_delete=models.CASCADE, blank=True, null=True)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, blank=True, null=True)
    # course_id = models.ForeignKey(CourseOverview, on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        app_label = "tnsdc_users"
        verbose_name = ('Student Details')
        verbose_name_plural = ('Student Details')

