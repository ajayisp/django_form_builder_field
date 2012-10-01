from django import forms

class CustomFormFieldInvalid(Exception):
    pass


field_type_to_django_form_field_mapping = {
     'small_text': forms.CharField(max_length=200),
     'large_text': forms.CharField(widget=forms.Textarea),
     'select_one': forms.ChoiceField(choices=()),
     'select_multiple': forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=()),
     'url': forms.URLField(),
     'email': forms.EmailField(),
     'number': forms.FloatField(),
     'date': forms.DateField(widget=forms.DateInput(attrs={'class':'date_input_box'})),
     'file': forms.FileField(),
     }


class FieldType(object):
    
    def __init__(self, field_type, field_display, associated_django_form_field=None, has_choices=False, css_class=None):        
        self.field_type = field_type
        self.field_display = field_display
        self.associated_django_form_field = associated_django_form_field or field_type_to_django_form_field_mapping[field_type]
        self.has_choices = has_choices
        self.css_class = css_class or field_type

SUPPORTED_FIELD_TYPES = (
    ('small_text', FieldType('small_text', 'Single line text')),
    ('large_text', FieldType('large_text', 'Paragraph text')),
    ('select_one', FieldType('select_one', 'Applicants choose one option from a list', has_choices=True)),
    ('select_multiple', FieldType('select_multiple', 'Applicants can choose multiple options', has_choices=True)),
    ('url', FieldType('url','Web-link / URL')),
    ('email', FieldType('email','Email Address')),
    ('number', FieldType('number', 'Number')),
    ('date', FieldType('date','Date')),
    ('file', FieldType('file','File Upload')),
)



def convert_to_field_type_object(type_of_field):
    for supported_field,supported_field_obj in SUPPORTED_FIELD_TYPES:
        if type_of_field == supported_field:
            return supported_field_obj
    raise CustomFormFieldInvalid('received an invalid type of field')


    

def create_django_form_field(field):    
    form_field = convert_to_field_type_object(field.get('field_type')).associated_django_form_field
    form_field.label = field.get('label')
    if field.get('value_options') is not None and len(field.get('value_options')) > 0:
        form_field.choices = [(a.strip(),a.strip()) for a in field.get('value_options')]
        if not field.get('is_required'):
            form_field.required=False
            if field.get('field_type') == 'select_one':
                # for select_one field type that is non-required, we must add a blank choice
                form_field.choices = [('','')] + form_field.choices
                form_field.initial = ''
    if field.get('is_required'):
        form_field.required = True
    else:
        form_field.required = False
    return form_field
