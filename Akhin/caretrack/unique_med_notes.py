import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caretrack.settings')
django.setup()

from patients.models import Medicine

def update_unique_descriptions():
    notes = [
        "Highly effective for immediate symptom relief. Store in a cool, dry place.",
        "Clinically proven fast-acting formula. Batch No: {batch}.",
        "Standard hospital-grade medication. Ref ID: {ref}.",
        "Recommended for adult use only. Monitor patient vitals during first dose.",
        "Essential medication for post-operative recovery phases.",
        "Used for broad-spectrum medical applications. Quality Certificate: {qc}.",
        "Effective for both acute and chronic conditions as prescribed.",
        "Maintains stable therapeutic levels when taken consistently.",
        "Premium quality formulation with high bioavailability.",
        "Indicated for specific healthcare needs. Verified Batch: {batch}."
    ]

    medicines = Medicine.objects.all()
    count = 0
    for med in medicines:
        random_note = random.choice(notes)
        unique_ref = f"B-{random.randint(100, 999)}-{med.id}"
        unique_qc = f"QC-{random.randint(10, 99)}"
        
        # Base description based on name categories
        base_desc = med.description if med.description and 'General medical' not in med.description else "Standard prescription for medical use."
        
        final_description = f"{base_desc} | {random_note.format(batch=unique_ref, ref=unique_ref, qc=unique_qc)}"
        
        med.description = final_description
        med.save()
        count += 1
    
    print(f"Successfully updated {count} medicines with unique detailed notes.")

if __name__ == '__main__':
    update_unique_descriptions()
