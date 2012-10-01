import factory
from form_field.models import ExampleModel

class ExampleModelFactory(factory.Factory):
    FACTORY_FOR = ExampleModel
    
    name = factory.Sequence(lambda n: 'example_model_{0}'.format(n))