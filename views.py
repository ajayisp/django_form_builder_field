from models import Demo
from django.http import HttpResponse
from django.shortcuts import render_to_response
from formfield.forms import FieldAsADjangoForm

def home(request):
    dm = Demo.objects.all()[0]
    field_forms = []
    for field in dm.all_fields:
        field_forms.append(FieldAsADjangoForm(field))
    
    if request.method == "POST":
        field_name = request.POST['name']
        for field_obj in dm.form.builder.fields:
            if field_name == field_obj.field['name']:
                field_form = field_obj.form(field, data=request.POST)
                if field_form.is_valid():
                    dm.form.edit('field_name', request.POST)
                return HttpResponse("Ciik")
                
        field_form = dm.form.builder.new_field_form(request.POST)
        if field_form.is_valid():
            dm.form.add_field(request.POST)
    
    return render_to_response('home.html', { 'field_forms':field_forms, 'new_field_form':FieldAsADjangoForm() })