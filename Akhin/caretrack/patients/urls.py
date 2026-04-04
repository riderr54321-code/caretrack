from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('delete-confirm/<int:id>/', views.delete_patient_confirm, name='delete_patient_confirm'),
    path('patient/<int:id>/', views.patient_details, name='patient_details'),
    path('qr/<int:id>/', views.generate_qr, name='generate_qr'),
    path('bill/<int:id>/', views.generate_bill, name='generate_bill'),
    path('deleted/', views.deleted_patients, name='deleted_patients'),
    path('restore/<int:id>/', views.restore_patient, name='restore_patient'),
    path('restore-confirm/<int:id>/', views.restore_patient_confirm, name='restore_patient_confirm'),
    path('reports/', views.reports, name='reports'),
    path('medicines/', views.medicines_list, name='medicines_list'),
    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('medicines/edit/<int:id>/', views.edit_medicine, name='edit_medicine'),
    path('medicines/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('settings/', views.settings_dashboard, name='settings_dashboard'),
    path('settings/equipment/add/', views.add_equipment, name='add_equipment'),
    path('settings/equipment/delete/<int:id>/', views.delete_equipment, name='delete_equipment'),
]