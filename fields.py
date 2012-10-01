from jsonfield import JSONField, JSON_DECODE_ERROR
from django.utils import simplejson as json
from forms import reduce_to_alphanumeric
from validation import create_django_form_field
from django.core.exceptions import ValidationError



class Fields(object):
    def __init__(self, fields, choose_initial_fields_from):
        self.fields = fields
        self.choose_initial_fields_from = choose_initial_fields_from

    @property
    def selected_fields(self):
        return self.fields        

    @property
    def all_fields(self):
        list_of_fields = []        
        for field in self.fields:
            if field.get('is_compulsory'):
                if not field.get('name'):
                    field['name'] = reduce_to_alphanumeric(unicode(field.get('label')).lower())
                list_of_fields.append({field['name']: field, 'is_choosen':True, 'is_compulsory':True, 'is_predefined':True, 'is_userdefined':False})

        for field in self.choose_initial_fields_from:
            if not field.get('is_compulsory'):
                if field in self.fields:
                    list_of_fields.append({field['name']: field, 'is_choosen':True, 'is_compulsory':False, 'is_predefined':True, 'is_userdefined':False})
                else:
                    list_of_fields.append({field['name']: field, 'is_choosen':False, 'is_compulsory':False, 'is_predefined':True, 'is_userdefined':False})


        for field in self.fields:
            if field not in self.choose_initial_fields_from:
                list_of_fields.append({field['name']: field, 'is_choosen':True, 'is_compulsory':False, 'is_predefined':False, 'is_userdefined':True})
        return list_of_fields

    # def validate_field(self, field):        
    #     for f in self.fields:
    #         if f['name'] == field['name']:
    #             raise ValidationError(" Already a field with same 'name' exists ")
    #     return True


    # def add_field(self, field):
    #     if not field.get('name'):
    #         field['name'] = reduce_to_alphanumeric(unicode(field.get('label')).lower())
    #     if self.validate_field(field):
    #         self.fields.append(field)
            

    # def set_fields(self, fields):
    #     old_fields = self.fields
    #     self.fields = []
    #     for f in fields:
    #         if not f.get('name'):
    #             f['name'] = reduce_to_alphanumeric(unicode(f.get('label')).lower())
    #         try:                
    #             if self.validate_field(f):
    #                 self.fields.append(fields)
    #         except Exception, e:
    #             self.fields = old_fields
    #             raise e

    # def remove_field(self, name):                
    #     for f in self.fields:
    #         if f['name'] == name:
    #             self.fields.remove(f)
    #             break

    # @property
    # def display_form(self):
    #     from collections import OrderedDict
    #     ret = OrderedDict()
        
    #     for f in self.fields:
    #         ret[f.get('label')] = create_django_form_field(f)
            
    #     display_form = DisplayForm()
    #     display_form.fields = ret
    #     return display_form
        

class FormField(JSONField):
    def __init__(self, *args, **kwargs):
        self.choose_initial_fields_from = kwargs.pop('choose_initial_fields_from', None)
        super(FormField, self).__init__(*args, **kwargs)
        self.default = None        

    def to_python(self, value):
        """
        Accepts only basestring or nonetype objects and depending on the type of value passed sets
        appropriate value to the field
        """
        from types import NoneType
        
        if isinstance(value, basestring):
            try:
                value = json.loads(value, **self.decoder_kwargs)             
            except JSON_DECODE_ERROR:
                pass

        elif isinstance(value, NoneType):
            # get the compulsory fields from the possible initial fields
            value = self.get_complusory_fields(self.choose_initial_fields_from)

            
        else:
            raise TypeError("Accepts only Basestring or NoneType objects for the value of %s" % self.name)

        value = Fields(value, self.choose_initial_fields_from)                

        return value

    def get_complusory_fields(self, choose_initial_fields_from):
        """
        Returns compulsory fields among the possible initial fields,
        decides on the basis of "is_compulsory" in the field(a dict object)        
        """        
        ret = []
        for field in choose_initial_fields_from:
            if field.get('is_compulsory'):
                ret.append(field)
        return ret
        
    def get_db_prep_value(self, value, *args, **kwargs):
        
        if isinstance(value, Fields):
            value = value.fields
        elif not value and self.choose_initial_fields_from:
            value = self.get_complusory_fields(self.choose_initial_fields_from)

        elif not value and not self.choose_initial_fields_from:
            pass
            
        else:
            raise TypeError("Use instance_obj.add_field to add fields ")

        return json.dumps(value, **self.encoder_kwargs)