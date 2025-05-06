from django.db import models
import uuid

class BaseUUIDModel(models.Model):
    """
    Base UUID model that represents a unique identifier for a given model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    # id = models.AutoField(primary_key=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=255, null = True, blank = True)
    created_by = models.CharField(max_length=255, null = True, blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True