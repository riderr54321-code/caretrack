from .models import HospitalSetting

def hospital_settings_processor(request):
    try:
        hospital_setting = HospitalSetting.load()
    except Exception:
        hospital_setting = None
    return {'hospital_setting': hospital_setting}
