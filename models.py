"""
Example models for testing the use of formfield
"""

from django.db import models
from fields import FormField

possible_initial_fields = [{'label': 'Name', 'name':'candidate_name', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':True},
       {'label': 'Email', 'name':'candidate_email', 'field_type':'email', 'field_description':'', 'is_required':True, 'is_compulsory':True , 'choices':None},
        {'label': 'Phone', 'name':'candidate_phone', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':True},
        {'label': 'linkedin', 'name':'candidate_linkedin', 'field_type':'url', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':False}        
]
 
class ExampleModel(models.Model):
    name = models.CharField(max_length=200)
    form = FormField(choose_initial_fields_from=possible_initial_fields)