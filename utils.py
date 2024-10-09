from model_utils.models import TimeStampedModel
from django.db import models
import uuid

class IsActiveModel(TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
