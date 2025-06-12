from django.db import models

# Create your models here.
class FinancialAidPartner(models.Model):
    COUNTRY_CHOICES=(
        ('india','india'),
        ('us','us')
    )
    partners = models.TextField(null=True,blank=True)
    country = models.TextField(null=True,blank=True,choices=COUNTRY_CHOICES)
    partnerlink = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.partners

class FinancialAidCourse(models.Model):
    course_id = models.CharField(max_length=100,null=True,blank=True)
    course_name = models.TextField(max_length=100,null=True,blank=True)
    financialpartners_india = models.ManyToManyField(FinancialAidPartner,blank=True,related_name="courses_india")
    financialpartners_us = models.ManyToManyField(FinancialAidPartner,blank=True,related_name="courses_us")

    def get_financialpartners_india(self):
        return ", ".join([fp.partners for fp in self.financialpartners_india.all()])

    def get_financialpartners_us(self):
        return ", ".join([fp.partners for fp in self.financialpartners_us.all()])


class FinancialAidProgram(models.Model):
    program_slug = models.CharField(max_length=100,null=True,blank=True)
    program_name = models.TextField(max_length=100,null=True,blank=True)
    financialpartners_india = models.ManyToManyField(FinancialAidPartner,blank=True,related_name="programs_india")
    financialpartners_us = models.ManyToManyField(FinancialAidPartner,blank=True,related_name="programs_us")

    def get_financialpartners_india(self):
        return ", ".join([fp.partners for fp in self.financialpartners_india.all()])

    def get_financialpartners_us(self):
        return ", ".join([fp.partners for fp in self.financialpartners_us.all()])