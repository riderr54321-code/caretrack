import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caretrack.settings')
django.setup()

from patients.models import Medicine

def generate_description(name):
    name_lower = name.lower()
    if 'paracetamol' in name_lower or 'dolo' in name_lower or 'calpol' in name_lower or 'crocin' in name_lower:
        return 'Analgesic and antipyretic. Used for pain relief and reducing fever.'
    if 'amoxicillin' in name_lower or 'azithromycin' in name_lower or 'antibiotic' in name_lower or 'ciprox' in name_lower:
        return 'Antibiotic medication used to treat a number of bacterial infections.'
    if 'cough' in name_lower or 'syrup' in name_lower or 'benadryl' in name_lower:
        return 'Used to relieve coughs caused by the common cold, bronchitis, and other breathing illnesses.'
    if 'pantoprazole' in name_lower or 'omeprazole' in name_lower or 'gelusil' in name_lower or 'digene' in name_lower:
        return 'Antacid/Proton pump inhibitor. Used to treat stomach ulcers, GERD, and high stomach acid.'
    if 'vitamin' in name_lower or 'neurobion' in name_lower or 'calcium' in name_lower or 'zinc' in name_lower:
        return 'Daily dietary supplement used to treat or prevent nutritional deficiencies.'
    if 'cetirizine' in name_lower or 'allegra' in name_lower or 'allergy' in name_lower or 'cold' in name_lower:
        return 'Antihistamine used to relieve allergy symptoms such as watery eyes, runny nose, and sneezing.'
    if 'metformin' in name_lower or 'insulin' in name_lower or 'glycomet' in name_lower:
        return 'Used to improve blood sugar control in people with type 2 diabetes.'
    if 'amlodipine' in name_lower or 'telmisartan' in name_lower or 'losartan' in name_lower:
        return 'Used to treat high blood pressure (hypertension) to prevent heart attacks and strokes.'
    if 'ibugesic' in name_lower or 'ibuprofen' in name_lower or 'combiflam' in name_lower or 'diclofenac' in name_lower:
        return 'Nonsteroidal anti-inflammatory drug (NSAID) used for reducing pain, inflammation, and stiffness.'
    if 'dropper' in name_lower or 'drops' in name_lower:
        return 'Medical eye/ear drops for localized treatment. Use exactly as prescribed.'
    if 'ointment' in name_lower or 'cream' in name_lower or 'betadine' in name_lower or 'gel' in name_lower:
        return 'Topical medication for external use applied directly to the affected skin area.'
    if 'injection' in name_lower:
        return 'Medication to be administered intravenously or intramuscularly strictly by a healthcare professional.'
    
    return 'General medical prescription. Please review patient history before administering and follow the prescribed dosage carefully.'

def update_descriptions():
    medicines = Medicine.objects.all()
    count = 0
    for med in medicines:
        med.description = generate_description(med.name)
        med.save()
        count += 1
    print(f"Successfully added descriptions for {count} medicines.")

if __name__ == '__main__':
    update_descriptions()
