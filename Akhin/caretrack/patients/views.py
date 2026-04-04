from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Medicine, UserProfile, HospitalSetting, Equipment


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role', 'doctor')
        if form.is_valid():
            user = form.save()
            # Create or update UserProfile with selected role
            userprofile, created = UserProfile.objects.get_or_create(user=user)
            userprofile.role = role
            userprofile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'patients/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'patients/login.html', {'error': 'Invalid credentials'})
    return render(request, 'patients/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    search_query = request.GET.get('search', '')
    filter_gender = request.GET.get('gender', '')
    filter_diagnosis = request.GET.get('diagnosis', '')
    filter_age = request.GET.get('age', '')

    # Only show non-deleted patients
    patients = Patient.objects.filter(is_deleted=False)

    if search_query:
        patients = patients.filter(name__icontains=search_query) | \
                   patients.filter(phone__icontains=search_query)

    if filter_gender:
        patients = patients.filter(gender=filter_gender)

    if filter_diagnosis:
        patients = patients.filter(diagnosis__icontains=filter_diagnosis)

    if filter_age:
        try:
            filter_age = int(filter_age)
            patients = patients.filter(age=filter_age)
        except ValueError:
            pass

    context = {
        'patients': patients,
        'search_query': search_query,
        'filter_gender': filter_gender,
        'filter_diagnosis': filter_diagnosis,
        'filter_age': filter_age,
    }
    return render(request, 'patients/home.html', context)


@login_required(login_url='login')
def add_patient(request):
    if request.method == 'POST':
        patient = Patient.objects.create(
            name=request.POST['name'],
            age=request.POST['age'],
            gender=request.POST['gender'],
            phone=request.POST['phone'],
            diagnosis=request.POST['diagnosis'],
            description=request.POST.get('description', ''),
            doctor_fee=request.POST.get('doctor_fee', 0.00),
        )

        # Handle medicines
        medicines_ids = request.POST.getlist('medicines')
        if medicines_ids:
            patient.medicines.set(medicines_ids)

        return redirect('home')

    medicines = Medicine.objects.all()
    ages = range(1, 101)

    context = {
        'medicines': medicines,
        'ages': ages,
    }
    return render(request, 'patients/add_patient.html', context)


@login_required(login_url='login')
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.name = request.POST['name']
        patient.age = request.POST['age']
        patient.gender = request.POST['gender']
        patient.phone = request.POST['phone']
        patient.diagnosis = request.POST['diagnosis']
        patient.description = request.POST.get('description', '')
        patient.doctor_fee = request.POST.get('doctor_fee', 0.00)
        patient.save()

        # Handle medicines
        medicines_ids = request.POST.getlist('medicines')
        patient.medicines.set(medicines_ids)

        return redirect('home')

    medicines = Medicine.objects.all()
    ages = range(1, 101)

    context = {
        'patient': patient,
        'medicines': medicines,
        'ages': ages,
    }
    return render(request, 'patients/edit_patient.html', context)


@login_required(login_url='login')
def delete_patient_confirm(request, id):
    """Show delete confirmation page"""
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        patient.soft_delete()
        return redirect('home')

    return render(request, 'patients/delete_patient_confirm.html', {'patient': patient})


@login_required(login_url='login')
def delete_patient(request, id):
    """Quick delete (for backward compatibility)"""
    patient = get_object_or_404(Patient, id=id)
    patient.soft_delete()
    return redirect('home')


@login_required(login_url='login')
def deleted_patients(request):
    """View all soft-deleted patients"""
    patients = Patient.objects.filter(is_deleted=True).order_by('-deleted_at')
    return render(request, 'patients/deleted_patients.html', {'patients': patients})


@login_required(login_url='login')
def restore_patient_confirm(request, id):
    """Show restore confirmation page"""
    patient = get_object_or_404(Patient, id=id, is_deleted=True)

    if request.method == 'POST':
        patient.restore()
        return redirect('home')

    return render(request, 'patients/restore_patient_confirm.html', {'patient': patient})


@login_required(login_url='login')
def restore_patient(request, id):
    """Quick restore (for backward compatibility)"""
    patient = get_object_or_404(Patient, id=id, is_deleted=True)
    patient.restore()
    return redirect('home')


@login_required(login_url='login')
def patient_details(request, id):
    patient = get_object_or_404(Patient, id=id)
    medicines = patient.medicines.all()
    medicine_total = sum((m.cost or 0) for m in medicines)
    doctor_fee = patient.doctor_fee or 0
    total_amount = medicine_total + doctor_fee
    context = {
        'patient': patient,
        'medicines': medicines,
        'medicine_total': medicine_total,
        'doctor_fee': doctor_fee,
        'total_amount': total_amount,
    }
    return render(request, 'patients/patient_details.html', context)


@login_required(login_url='login')
def generate_qr(request, id):
    """Generate QR code for patient"""
    patient = get_object_or_404(Patient, id=id)

    # Get medicines
    medicines = patient.medicines.all()
    medicine_names = ', '.join([m.name for m in medicines])

    # Create QR data
    from django.urls import reverse
    qr_data = request.build_absolute_uri(reverse('patient_details', args=[patient.id]))

    # Try to generate QR code
    qr_image_b64 = None
    try:
        import qrcode
        from PIL import Image, ImageDraw, ImageFont
        import base64
        from io import BytesIO

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Add CareTrack logo
        try:
            img = img.convert('RGB')
            width, height = img.size
            draw = ImageDraw.Draw(img)

            # Draw white circle in center
            circle_size = 60
            x1 = (width - circle_size) // 2
            y1 = (height - circle_size) // 2
            x2 = x1 + circle_size
            y2 = y1 + circle_size
            draw.ellipse([x1, y1, x2, y2], fill='white')

            # Draw "CT" text
            text = "CT"
            font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            draw.text((text_x, text_y), text, fill='#1a3f47', font=font)
        except Exception as e:
            pass

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_image_b64 = base64.b64encode(buffer.getvalue()).decode()

    except ImportError:
        pass

    context = {
        'patient': patient,
        'medicines': medicines,
        'qr_image_b64': qr_image_b64,
    }
    return render(request, 'patients/qr_code.html', context)


@login_required(login_url='login')
def generate_bill(request, id):
    patient = get_object_or_404(Patient, id=id)
    medicines = patient.medicines.all()
    
    medicine_total = sum((m.cost or 0) for m in medicines)
    doctor_fee = patient.doctor_fee or 0
    total_amount = medicine_total + doctor_fee
    
    medicines_text = "\n".join([f"- {m.name}: ${m.cost}" for m in medicines])
    qr_text = f"Patient: {patient.name}\nAge/Gender: {patient.age}/{patient.gender}\nDiagnosis: {patient.diagnosis}\n" \
              f"Doctor Fee: ${doctor_fee}\nMedicines:\n{medicines_text}\n" \
              f"----------------\nTotal Amount: ${total_amount}"
              
    qr_image_b64 = None
    try:
        import qrcode
        import base64
        from io import BytesIO

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_image_b64 = base64.b64encode(buffer.getvalue()).decode()
    except ImportError:
        pass

    context = {
        'patient': patient,
        'medicines': medicines,
        'medicine_total': medicine_total,
        'total_amount': total_amount,
        'qr_image_b64': qr_image_b64,
    }
    return render(request, 'patients/generate_bill.html', context)


@login_required(login_url='login')
def reports(request):
    total_patients = Patient.objects.filter(is_deleted=False).count()
    deleted_patients = Patient.objects.filter(is_deleted=True).count()
    medicines_count = Medicine.objects.count()
    
    # Just a simple stat to show some numbers
    total_prescriptions = sum(p.medicines.count() for p in Patient.objects.filter(is_deleted=False))
    
    context = {
        'total_patients': total_patients,
        'deleted_patients': deleted_patients,
        'medicines_count': medicines_count,
        'total_prescriptions': total_prescriptions,
    }
    return render(request, 'patients/reports.html', context)


@login_required(login_url='login')
def medicines_list(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'patients/medicines_list.html', {'medicines': medicines})


@login_required(login_url='login')
def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        cost = request.POST.get('cost', 0.00)
        if name:
            Medicine.objects.create(name=name, description=description, cost=cost)
            return redirect('medicines_list')
    return render(request, 'patients/medicine_form.html', {'title': 'Add Medicine'})


@login_required(login_url='login')
def edit_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            medicine.name = name
            medicine.description = request.POST.get('description', '')
            medicine.cost = request.POST.get('cost', 0.00)
            medicine.save()
            return redirect('medicines_list')
    return render(request, 'patients/medicine_form.html', {'medicine': medicine, 'title': 'Edit Medicine'})


@login_required(login_url='login')
def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    return redirect('medicines_list')


@login_required(login_url='login')
def settings_dashboard(request):
    hospital_setting = HospitalSetting.load()
    equipments = Equipment.objects.all().order_by('-added_at')

    if request.method == 'POST':
        if 'update_hospital_settings' in request.POST:
            hospital_setting.hospital_name = request.POST.get('hospital_name', hospital_setting.hospital_name)
            hospital_setting.hospital_address = request.POST.get('hospital_address', hospital_setting.hospital_address)
            hospital_setting.contact_email = request.POST.get('contact_email', hospital_setting.contact_email)
            hospital_setting.contact_phone = request.POST.get('contact_phone', hospital_setting.contact_phone)
            hospital_setting.save()
            return redirect('settings_dashboard')

    context = {
        'hospital_setting': hospital_setting,
        'equipments': equipments,
    }
    return render(request, 'patients/settings_dashboard.html', context)


@login_required(login_url='login')
def add_equipment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'Available')
        
        if name:
            Equipment.objects.create(name=name, description=description, status=status)
    return redirect('settings_dashboard')


@login_required(login_url='login')
def delete_equipment(request, id):
    equipment = get_object_or_404(Equipment, id=id)
    equipment.delete()
    return redirect('settings_dashboard')
