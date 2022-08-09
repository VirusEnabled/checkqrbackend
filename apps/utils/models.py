from django.db import models
import uuid
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    """
    generic model
    """
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4,
                            editable=False)
    history = HistoricalRecords(inherit=True)


    class Meta:
        abstract = True
