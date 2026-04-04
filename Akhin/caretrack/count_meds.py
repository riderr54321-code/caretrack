import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caretrack.settings')
django.setup()
from patients.models import Medicine
print(f"COUNT:{Medicine.objects.count()}")
