from datetime import date


class DatabaseLoader:
    """
    This class is used to copy data linked to a certain company and link it to another given company
    It also copy all fks and change the parent object they point to.
    ...
     Constraints
    ----------
       - This class doesn't take into consideration many to many relationships.
       - Models to be copied should reside in Defenition module


    Attributes
    ----------
    model_name : str
        model name to copy data from
    from_company_id : int
        company id to copy data that are linked to it
    to_company_id : int
        company id that new copied data will link to it
    enterprise_field_name : str
        enterprise filed name in the parent model to copy data from

    Methods
    -------
    get_all_data():
      get all data to be copied and set it to the data attribute

    duplicate_data():
        copy data and link it to the given company id including all foreign keys pointing to it

    """

    def __init__(self, model_name, from_company_id, to_company_id, enterprise_field_name):
        self.model = model_name
        self.to_company_id = to_company_id
        self.from_company_id = from_company_id
        self.data = None
        self.enterprise_field = enterprise_field_name

    def get_all_data(self):
        from defenition import models
        # dynamically import model
        dynamic_model = getattr(models, self.model)
        all_data = dynamic_model.objects.filter(enterprise=self.from_company_id)
        self.data = all_data

    def duplicate_data(self):
        if self.data is None:
            self.get_all_data()
        for record in self.data:
            related_objects_to_copy = []
            # get all fields in the model object
            for field in record._meta.get_fields():
                # check if a field is a foreign key of type one to many
                if field.one_to_many:
                    try:
                        related_object_manager = getattr(record, field.name)
                        related_objects = list(related_object_manager.all())
                    # exception will be raised in case no data exists for the field
                    except AttributeError:
                        related_objects = []
                    if related_objects:
                        related_objects_to_copy += related_objects
            # following django docs in copying an object
            record.pk = None
            # set the company this object is linked to
            setattr(record, self.enterprise_field, self.to_company_id)
            record.start_date = date.today()
            record.end_date = None
            record.creation_date = None
            record.last_update_by = None
            record.save()
            # loop on all fks pointing to the old object and copying them with new parent object
            for related_object in related_objects_to_copy:
                for related_object_field in related_object._meta.fields:
                    if related_object_field.related_model == record.__class__:
                        related_object.pk = None
                        related_object.start_date = date.today()
                        related_object.end_date = None
                        related_object.creation_date = None
                        related_object.last_update_by = None
                        # change the old parent id to point to the new parent
                        setattr(related_object, related_object_field.name, record)
                        related_object.save()
