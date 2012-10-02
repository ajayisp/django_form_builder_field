from django import forms
from utils import reduce_to_alphanumeric                                


field_type_choices = (
		('small_text','Single line text'),
		('large_text','Paragraph text'),
		('select_one','Applicants choose one option from a list'),
		('select_multiple','Applicants can choose multiple options'),
		('url','Web-link / URL'),
		('email','Email Address'),
		('number', 'Number'),
		('date','Date'),
		('file','File Upload'),
)


class FieldAsADjangoForm(forms.Form):
	label = forms.CharField(max_length=400, label="Question/Title")
	description = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), required=False, label="Help Text")
	field_type = forms.ChoiceField(choices=field_type_choices, initial=field_type_choices[0][0], label="Answer Type", widget=forms.Select())
	is_required = forms.BooleanField(initial=False, required=False, label="Answer Mandatory?", widget=forms.CheckboxInput())
	value_options = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=())
        name = forms.CharField(widget=forms.HiddenInput(), required=False)        
        

        def __init__(self, field=None, *args, **kwargs):
            super(FieldAsADjangoForm, self).__init__(*args, **kwargs)
            self.field = field
            if field:
                self.fields['label'].initial = field.get('label')
                self.fields['description'].initial = field.get('field_description')
                self.fields['field_type'].initial = field.get('field_type')                
                self.fields['is_required'].initial = field.get('is_required')                
                self.fields['name'].initial = field.get('name')
                
                if field.get('is_compulsory', False):
                    self.fields['field_type'].widget.attrs['disabled'] = "disabled"
                    self.fields['is_required'].widget.attrs['disabled'] = "disabled"
                    self.fields['value_options'].widget.attrs['disabled'] = "disabled"

                if field.get('choices'):
                    self.fields['value_options'].choices = [(opt,opt) for opt in field.get('choices')]
                    self.fields['value_options'].initial = field.get('choices')
                    

        def clean(self):
            cleaned_data = super(FieldAsADjangoForm, self).clean()
            field_type = cleaned_data.get("field_type")
            value_options = cleaned_data.get("value_options")
            if field_type == "select_one" or field_type == "select_multiple":
                if not len(value_options):
                    raise forms.ValidationError(" if the field_type is select_one or select_multiple then value_options shouldnt be empty, error for field with label %s" % self.field.get("label"))
                    
            return cleaned_data

class DisplayForm(forms.Form):
        pass