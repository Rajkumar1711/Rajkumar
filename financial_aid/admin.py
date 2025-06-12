from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib import admin
from financial_aid.models import *

# Register your models here.
class FinancialAidCourseForm(forms.ModelForm):
    class Meta:
        model =  FinancialAidCourse
        fields = '__all__'
    financialpartners_india = forms.ModelMultipleChoiceField( queryset=FinancialAidPartner.objects.filter(country='india'), widget = FilteredSelectMultiple('financialpartners_india', is_stacked=False), )
    financialpartners_us = forms.ModelMultipleChoiceField( queryset=FinancialAidPartner.objects.filter(country='us'), widget = FilteredSelectMultiple('financialpartners_us', is_stacked=False), )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['financialpartners_india'].required = False
        self.fields['financialpartners_us'].required = False

class FinancialAidProgramForm(forms.ModelForm):
    class Meta:
        model =  FinancialAidPartner
        fields = '__all__'
    financialpartners_india = forms.ModelMultipleChoiceField( queryset=FinancialAidPartner.objects.filter(country='india'), widget = FilteredSelectMultiple('financialpartners_india', is_stacked=False), )
    financialpartners_us = forms.ModelMultipleChoiceField( queryset=FinancialAidPartner.objects.filter(country='us'), widget = FilteredSelectMultiple('financialpartners_us', is_stacked=False), )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['financialpartners_india'].required = False
        self.fields['financialpartners_us'].required = False

class FinancialAidPartnerAdmin(admin.ModelAdmin):
    list_display = ['partners','country','partnerlink']

class FinancialAidCourseAdmin(admin.ModelAdmin):
    form = FinancialAidCourseForm
    filter_horizontal= ('financialpartners_india','financialpartners_us',)
    list_display = ['course_id','course_name','get_financialpartners_india','get_financialpartners_us']

class FinancialAidProgramAdmin(admin.ModelAdmin):
    form = FinancialAidProgramForm
    filter_horizontal= ('financialpartners_india','financialpartners_us',)
    list_display = ['program_slug','program_name','get_financialpartners_india','get_financialpartners_us']


admin.site.register(FinancialAidPartner,FinancialAidPartnerAdmin)
admin.site.register(FinancialAidCourse,FinancialAidCourseAdmin)
admin.site.register(FinancialAidProgram,FinancialAidProgramAdmin)
