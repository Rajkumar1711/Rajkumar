# from django.db import models
# from django.db.models import Q
# #models here

# class Course(models.Model):
#     id = models.AutoField(primary_key=True)
#     college_name = models.CharField(max_length=255,null=True,blank=True)
#     # tech_id = models.ForeignKey(Technologies, on_delete=models.CASCADE,null=True,blank=True)
#     group = models.CharField(max_length=100,null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.college_name)

#     class Meta(object):
#         verbose_name = 'Courses'
#         verbose_name_plural = 'Courses'

# # class Technologies(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     tech_name = models.CharField(max_length=255,null=True,blank=True)
# #     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
# #     created_time = models.DateTimeField(auto_now_add=True)
# #     updated_time = models.DateTimeField(auto_now=True)

# #     def __str__(self):
# #         return str(self.college_name)

# #     class Meta(object):
# #         verbose_name = 'Technologies'
# #         verbose_name_plural = 'Technologies'

# class College(models.Model):
#     id = models.AutoField(primary_key=True)
#     college_code = models.CharField(max_length=100,null=True,blank=True)
#     college_name = models.CharField(max_length=255,null=True,blank=True)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     team_size = models.IntegerField(null=True,blank=True)
#     student_count = models.IntegerField(null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.college_name)

#     class Meta(object):
#         verbose_name = 'Colleges'
#         verbose_name_plural = 'Colleges'

# class Branch(models.Model):
#     id = models.AutoField(primary_key=True)
#     branch_name = models.CharField(max_length=255,null=True,blank=True)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     # tech_id = models.ForeignKey(Technologies, on_delete=models.CASCADE,null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.college_name)

#     class Meta(object):
#         verbose_name = 'Technologies'
#         verbose_name_plural = 'Technologies'


# class Project(models.Model):
#     id = models.AutoField(primary_key=True)
#     project_name = models.TextField(null=True,blank=True)
#     project_description = models.TextField(null=True,blank=True)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     college_id = models.ForeignKey(College, on_delete=models.CASCADE,null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     # def get_college(self):
#     #     return ", ".join([fp.college_name for fp in self.college.all()])

#     def __str__(self):
#         return str(self.project_name)

#     class Meta(object):
#         verbose_name = 'Projects'
#         verbose_name_plural = 'Projects'


# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField(max_length=100,unique=True)
#     first_name = models.CharField(max_length=100,null=True,blank=True)
#     last_name = models.CharField(max_length=100,null=True,blank=True)
#     role = models.CharField(max_length=30,null=True,blank=True, choices=[("Team Member", "Team Member"), ("Team Mentor", "Team Mentor"), ("Spoc", "Spoc"), ("Evaluator", "Evaluator"), ("Principal", "Principal"), ("Admin", "Admin")])
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         # return (self.first_name or "") + " "+ (self.last_name or "")
#         return self.email

#     class Meta(object):
#         verbose_name = 'Users'
#         verbose_name_plural = 'Users'

# class Users_info(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User,related_name="u_id", on_delete=models.CASCADE)
#     nm_id = models.CharField(max_length=100,null=True,blank=True)
#     branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE,null=True,blank=True)
#     college_id = models.ForeignKey(College, on_delete=models.CASCADE,null=True,blank=True)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     is_evaluator = models.BooleanField(default=False)
#     eval_course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     anna_univ_id = models.CharField(max_length=100,null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         # return (self.first_name or "") + " "+ (self.last_name or "")
#         return self.email

#     class Meta(object):
#         verbose_name = 'Users_info'
#         verbose_name_plural = 'Users_info'

# class Session(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User,related_name="u_id", on_delete=models.CASCADE)
#     college_id = models.ForeignKey(College, on_delete=models.CASCADE,null=True,blank=True)
#     course_id = models.ForeignKey(Course, on_delete=models.CASCADE,null=True,blank=True)
#     start_date = models.DateField(('Course Start Date'))
#     end_date = models.DateField(('Course End Date'))
#     updated_time = models.DateTimeField(auto_now=True)
#     batch = models.CharField(max_length=30,null=True,blank=True, choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")])
#     year = models.CharField(max_length=30,null=True,blank=True, choices=[("2023", "2023"), ("2024", "2024")])


#     def __str__(self):
#         # return (self.first_name or "") + " "+ (self.last_name or "")
#         return self.id

#     class Meta(object):
#         verbose_name = 'Session'
#         verbose_name_plural = 'Session'


# class Team(models.Model):
#     id = models.AutoField(primary_key=True)
#     team_name = models.CharField(max_length=255,null=True,blank=True)
#     members_user_id = models.ForeignKey(User,related_name="u_id", on_delete=models.CASCADE)
#     mentor_user_id = models.ForeignKey(User,related_name="u_id", on_delete=models.CASCADE)
#     eval_user_id = models.ForeignKey(User,related_name="u_id", on_delete=models.CASCADE)
#     project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
#     session_id = models.ForeignKey(Session, on_delete=models.CASCADE,null=True,blank=True)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)
#     # mentor = models.ForeignKey(User,blank=True, related_name="teams_mentors", on_delete=models.CASCADE, limit_choices_to={"role": "Team Mentor"},null=True)
#     # members = models.ManyToManyField(User,blank=True, related_name="teams_members", limit_choices_to={"role": "Team Member"})
#     # evaluator = models.ForeignKey(User,blank=True,related_name="teams_evaluator", on_delete=models.CASCADE, limit_choices_to=Q(role="Evaluator") | Q(role="Team Mentor"),null=True)

#     # def get_members(self):
#     #     return ", ".join([fp.email for fp in self.members.all()])

#     def __str__(self):
#         return self.team_name

#     class Meta(object):
#         verbose_name = 'Teams'
#         verbose_name_plural = 'Teams'


# # class TnsdcEnrollment(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     course_id = models.CharField(max_length=100,null=True,blank=True)
# #     email = models.ForeignKey(User,blank=True,null=True,related_name="enrollment", on_delete=models.CASCADE)
# #     is_enrolled = models.BooleanField(default=False)
# #     is_registered = models.BooleanField(default=True)

# #     def __str__(self):
# #         return "__all__"

# #     class Meta(object):
# #         verbose_name = 'TnsdcEnrollments'
# #         verbose_name_plural = 'TnsdcEnrollments'


# class TnsdcSubmission(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User,related_name="submission", on_delete=models.CASCADE)
#     team_id = models.ForeignKey(Team,on_delete=models.CASCADE,related_name="user_team",null=True,blank=True)
#     phase1_submitted = models.BooleanField(default=False)
#     eval_a1= models.FloatField(default=0.0)
#     eval_a2= models.FloatField(default=0.0)
#     avg1 = models.FloatField(default=0.0)
#     phase2_submitted = models.BooleanField(default=False)
#     eval_b1= models.FloatField(default=0.0)
#     eval_b2= models.FloatField(default=0.0)
#     avg2 = models.FloatField(default=0.0)
#     phase3_submitted = models.BooleanField(default=False)
#     eval_c1= models.FloatField(default=0.0)
#     eval_c2= models.FloatField(default=0.0)
#     avg3 = models.FloatField(default=0.0)
#     phase4_submitted = models.BooleanField(default=False)
#     eval_d1= models.FloatField(default=0.0)
#     eval_d2= models.FloatField(default=0.0)
#     avg4 = models.FloatField(default=0.0)
#     phase5_submitted = models.BooleanField(default=False)
#     eval_e1= models.FloatField(default=0.0)
#     eval_e2= models.FloatField(default=0.0)
#     avg5 = models.FloatField(default=0.0)
#     final_submission = models.BooleanField(default=False)
#     final_marks = models.FloatField(default=0.0)
#     final_remark = models.FloatField(default=0.0)
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return "__all__"

#     class Meta(object):
#         unique_together = (("email"),)
#         verbose_name = 'TnsdcSubmissions'
#         verbose_name_plural = 'TnsdcSubmissions'
