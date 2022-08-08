from django.db import models
import uuid
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    """
    generic model
    """
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)
    history = HistoricalRecords()


    class Meta:
        abstract = True
