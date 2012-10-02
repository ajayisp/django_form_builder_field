from jsonfield import JSONField, JSON_DECODE_ERROR
from django.utils import simplejson as json
from utils import reduce_to_alphanumeric
from validation import create_django_form_field
from forms import DisplayForm


class FormFieldsDataStructure(list):

    @property
    def raw_fields(self):
        raw_fields_list = []
        for field in self:
            raw_fields_list.append(field['field_details'])
        return raw_fields_list

    def __contains__(self, item):
        ret_value = super(FormFieldsDataStructure,self).__contains__(item)
        if not ret_value:
            for field in self:
                if field['field_details']['name'] == item:
                    return True
        return ret_value
        

class Fields(object):
    def __init__(self, fields, choose_initial_fields_from):
        self.fields = fields
        self.choose_initial_fields_from = choose_initial_fields_from

    @property
    def selected_fields(self):
        """
        Returns the list of selected field choosen by the user
        """
        return self.fields

    @property
    def all_fields(self):
        """
        Returns all the fields compulsory, predefined, user defined
        both choosen and not choosen fields
        This is used for getting all the fields so that
        the application form creating form can be constructed
        """
        
        list_of_fields = FormFieldsDataStructure()

        for field in self.fields:
            field['name'] = field.get('name', reduce_to_alphanumeric(unicode(field.get('label')).lower()))            
            if field.get('is_compulsory'):                
                list_of_fields.append({'field_details': field, 'meta': {'is_choosen':True, 'is_compulsory':True, 'is_predefined':True, 'is_userdefined': False}})

        for field in self.choose_initial_fields_from:
            if not field.get('is_compulsory'):
                if field in self.fields:
                    list_of_fields.append({'field_details': field, 'meta': {'is_choosen':True, 'is_compulsory':False, 'is_predefined':True, 'is_userdefined':False}})
                else:
                    list_of_fields.append({'field_details': field, 'meta': {'is_choosen':False, 'is_compulsory':False, 'is_predefined':True, 'is_userdefined':False}})


        for field in self.fields:
            if field not in self.choose_initial_fields_from:
                list_of_fields.append({'field_details': field, 'meta': {'is_choosen':True, 'is_compulsory':False, 'is_predefined':False, 'is_userdefined':True}})
        return list_of_fields

    def validate_field(self, field):
        """
        Does validation on all the fields
        """
        for f in self.fields:
            if f['name'] == field['name']:
                raise ValueError(" Already a field with same 'name' exists ")
        return True


    def add_field(self, field):
        """
        Adds a new field to the list of fields 'self.fields' after validating
        Returns True if the field is successfully added or throws
        ValueError instead (if validation or something fails)
        """
        if not field.get('name'):
            field['name'] = reduce_to_alphanumeric(unicode(field.get('label')).lower())
            
        if self.validate_field(field):
            self.fields.append(field)
            
        return True

    def edit_field(self, name, new_field_details):
        field_to_edit = None
        for field  in self.fields:
            if field['name'] == name:
                field_to_edit = field
                break

        if not field_to_edit:
            raise ValueError("Field with name %s not found " % name)

        if field_to_edit.get('is_compulsory', False):
            for key in field_to_edit.keys():
                if (field_to_edit.get(key) != new_field_details.get(key)) and key != "label":
                    raise ValueError("Only label attribute on a compulsory field is allowed to be editied not the other ones")
                    
        pos_to_insert  = self.fields.index(field_to_edit)
        self.fields[pos_to_insert] = new_field_details


    def remove_field(self, name):
        """
        Removes a field from the list when its name is provided
        Returns true anyways
        """
        for f in self.fields:
            if f['name'] == name:
                if f.get('is_compulsory', False):
                    raise ValueError("Cannot remove a compulsory Field")
                self.fields.remove(f)
                break
        return True
        

        

class FormField(JSONField):
    def __init__(self, *args, **kwargs):
        # look for field list to choose intial fields from 
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
        """
        Only the choosen fields go in the database,
        only the field_details of field go in database

        """
        
        if isinstance(value, Fields):
            value = value.fields
        elif not value and self.choose_initial_fields_from:
            value = self.get_complusory_fields(self.choose_initial_fields_from)

        elif not value and not self.choose_initial_fields_from:
            pass
            
        else:
            raise TypeError("Use instance_obj.add_field to add fields ")

        return json.dumps(value, **self.encoder_kwargs)