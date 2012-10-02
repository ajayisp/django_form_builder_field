"""
Tests the custom fields in the project
"""
from django.test import TestCase
from factories import ExampleModelFactory


class FormFieldTestCase(TestCase):
    """
    Tests the formfield (a custom field for creating forms and attaching to model instances)
    """

    def setUp(self):
        # create model instance which uses the formfield
        self.model_instance = ExampleModelFactory()

    def test_form_field_initialization(self):
        """
        Test the initialization of the formfield,
        check if 'selected_fields' attribute on form returns the
        right fields from the possible initial fields passed to it
        i.e. the fields which are compulsory
        
        """        
        from form_field.models import possible_initial_fields
        selected_fields = []
        for fields in possible_initial_fields:
            if fields.get('is_compulsory'):
                selected_fields.append(fields)        

        self.assertEqual(self.model_instance.form.selected_fields, selected_fields)


    def test_form_field_initialization_2(self):
        """
        Test the initialization of the formfield,
        check if 'all_fields' attribute behaves as expected        
        """
        from form_field.models import possible_initial_fields

        field_dict = {'field_details': possible_initial_fields[0], 'meta':{'is_choosen':True, 'is_compulsory':True, 'is_predefined':True, 'is_userdefined':False}}
        # all_fields should be a list of field_dict type objects
        self.assertTrue(field_dict in self.model_instance.form.all_fields)        

        #raw_fields attribute should return the list of all the fields both compulsory and not compulsory
        self.assertEqual(self.model_instance.form.all_fields.raw_fields, possible_initial_fields)

        # should check if any field with a given name  is in the list
        self.assertTrue(possible_initial_fields[0]['name'] in self.model_instance.form.all_fields)



    def test_add_field(self):
        """
        Add a new field to the form and check the behaviour
        """
        new_field = {'label': 'github', 'name':'candidate_github', 'field_type':'url', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory': False}
        self.assertTrue(self.model_instance.form.add_field(new_field))

        # should raise ValueError if a same field is added again
        self.assertRaises(ValueError, self.model_instance.form.add_field, new_field)

        field_dict = { 'field_details': new_field, 'meta':{'is_choosen':True, 'is_compulsory':new_field['is_compulsory'], 'is_predefined':False, 'is_userdefined':True} }
        
        #all_fields attribute to should have new_field in it
        self.assertTrue(field_dict in self.model_instance.form.all_fields)

        #field should be in the selected fields
        self.assertTrue(new_field in self.model_instance.form.selected_fields)

    def test_remove_field(self):
        """
        Remove a field from the form and check the behaviour
        """
        field = {'label': 'location', 'name':'candidate_location', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory': False}
        
        # add the field to form
        self.model_instance.form.add_field(field)
        
        #remove the above field from the form
        self.assertTrue(self.model_instance.form.remove_field(field['name']))

        # check if the field has been removed
        self.assertFalse(field in self.model_instance.form.selected_fields)

        #should raise ValueError if an attempt is made to remove a compulsory field

        compulsory_field = {'label': 'workplace', 'name':'candidate_workplace', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory': True}
        self.model_instance.form.add_field(compulsory_field)        
        self.assertRaises(ValueError, self.model_instance.form.remove_field, compulsory_field['name'])


    # def test_set_fields(self):
    #     """
    #     Test the setting of the forms fields to new values
    #     """
        
    #     new_fields = [{'label': 'age', 'name':'candidate_age', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':True},
    #     {'label': 'height', 'name':'candidate_height', 'field_type':'email', 'field_description':'', 'is_required':True, 'is_compulsory':True , 'choices':None},
    #     {'label': 'weight', 'name':'candidate_weight', 'field_type':'small_text', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':True},
    #     {'label': 'facebook', 'name':'candidate_facebook', 'field_type':'url', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory':False}
    #     ]
    #     #set the new fields
    #     self.model_instance.form.set_fields(new_fields)
        
    #     # hit save to reflect in database
    #     self.model_instance.save()
        
    #     print self.model_instance.form.fields
    #     self.assertEqual(self.model_instance.form.all_fields.raw_fields, new_fields)

    def test_edit_field(self):
        """
        Tests the edit_field function on formfield 
        """
        field = {'label': 'age', 'name':'candidate_age', 'field_type':'number', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory': False}
        
        # add the above field to the form
        self.model_instance.form.add_field(field)

        #update the field
        from copy import deepcopy
        modified_field = deepcopy(field)
        modified_field['field_description'] = "this is the modified field"
        
        #now replace the earlier field        
        self.model_instance.form.edit_field(modified_field['name'], modified_field)

        #check for the existence of the modified field in fields list
        self.assertTrue(modified_field in self.model_instance.form.all_fields.raw_fields)

        #should raise ValueError if the name of field to edit is not found
        with self.assertRaises(ValueError):
            self.model_instance.form.edit_field("somethingsomething", modified_field)

        # create a compulsory field
        compulsory_field = {'label': 'height', 'name':'candidate_height', 'field_type':'number', 'field_description':'', 'is_required':True, 'choices':None, 'is_compulsory': True}
        self.model_instance.form.add_field(compulsory_field)

        #change the description of the compulsoryfield
        modified_compulsory_field = deepcopy(compulsory_field)
        modified_compulsory_field["field_description"] = "this is the modified compulsory field"
        
        with self.assertRaises(ValueError):
            self.model_instance.form.edit_field(modified_compulsory_field['name'], modified_compulsory_field)        
        

