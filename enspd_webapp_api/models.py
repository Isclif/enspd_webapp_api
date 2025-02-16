from django.db import models

class BaseUUIDModel(models.Model):
    """
    Base UUID model that represents a unique identifier for a given model.
    """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    id = models.AutoField(primary_key=True)
    
    
    time_created = models.DateTimeField(auto_now_add=True)
    employee_updater = models.CharField(max_length=255, null = True, blank = True)
    time_updated = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True