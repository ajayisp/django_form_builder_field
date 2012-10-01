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
        check if 'all_fields' attribute on form returns all the
        fields i.e. compulsory as well as not compulsory fields        
        """
        from form_field.models import possible_initial_fields
        # order may change but still it's valid  so use multisets
        self.assertEqual(dict(self.model_instance.form.all_fields), dict(possible_initial_fields))
