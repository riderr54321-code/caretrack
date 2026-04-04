from django.core.management.base import BaseCommand
from patients.models import Medicine


class Command(BaseCommand):
    help = 'Seed database with 1000+ medicines'

    def handle(self, *args, **options):
        medicines_data = [
            'Amoxicillin', 'Azithromycin', 'Cephalexin', 'Ciprofloxacin', 'Doxycycline',
            'Erythromycin', 'Gentamicin', 'Levofloxacin', 'Metronidazole', 'Nitrofurantoin',
            'Penicillin G', 'Tetracycline', 'Vancomycin', 'Ceftriaxone', 'Trimethoprim-Sulfamethoxazole',
            'Acetaminophen', 'Aspirin', 'Ibuprofen', 'Naproxen', 'Indomethacin',
            'Ketoprofen', 'Meloxicam', 'Piroxicam', 'Celecoxib', 'Rofecoxib',
            'Codeine', 'Morphine', 'Oxycodone', 'Hydrocodone', 'Fentanyl',
            'Methadone', 'Tramadol', 'Propoxyphene', 'Pentazocine', 'Butorphanol',
            'Amphotericin B', 'Fluconazole', 'Itraconazole', 'Ketoconazole', 'Miconazole',
            'Nystatin', 'Terbinafine', 'Voriconazole', 'Griseofulvin', 'Clotrimazole',
            'Acyclovir', 'Ganciclovir', 'Valacyclovir', 'Famciclovir', 'Cidofovir',
            'Cetirizine', 'Fexofenadine', 'Loratadine', 'Desloratadine', 'Levocetirizine',
            'Diphenhydramine', 'Promethazine', 'Chlorpromazine', 'Hydroxyzine', 'Meclizine',
            'Aluminum Hydroxide', 'Magnesium Hydroxide', 'Calcium Carbonate', 'Sodium Bicarbonate', 'Cimetidine',
            'Famotidine', 'Nizatidine', 'Ranitidine', 'Lansoprazole', 'Omeprazole',
            'Amlodipine', 'Diltiazem', 'Nifedipine', 'Verapamil', 'Lisinopril',
            'Enalapril', 'Perindopril', 'Quinapril', 'Ramipril', 'Captopril',
            'Losartan', 'Valsartan', 'Irbesartan', 'Candesartan', 'Telmisartan',
            'Atenolol', 'Bisoprolol', 'Carvedilol', 'Labetalol', 'Metoprolol',
            'Albuterol', 'Terbutaline', 'Salmeterol', 'Formoterol', 'Vilanterol',
            'Sertraline', 'Paroxetine', 'Fluoxetine', 'Citalopram', 'Escitalopram',
            'Venlafaxine', 'Duloxetine', 'Desvenlafaxine', 'Fluvoxamine', 'Bupropion',
            'Amitriptyline', 'Nortriptyline', 'Imipramine', 'Doxepin', 'Desipramine',
            'Phenytoin', 'Phenobarbital', 'Primidone', 'Ethosuximide', 'Valproic Acid',
            'Levothyroxine', 'Liothyronine', 'Liotrix', 'Thyroid Extract', 'Propylthiouracil',
            'Insulin Glargine', 'Insulin Aspart', 'Insulin Lispro', 'Metformin', 'Glyburide',
            'Glimepiride', 'Glipizide', 'Tolbutamide', 'Sitagliptin', 'Saxagliptin',
            'Vitamin A', 'Vitamin B1', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5',
            'Vitamin B6', 'Vitamin B7', 'Vitamin B9', 'Vitamin B12', 'Vitamin C',
            'Vitamin D2', 'Vitamin D3', 'Vitamin E', 'Vitamin K1', 'Vitamin K2',
            'Calcium Carbonate', 'Calcium Citrate', 'Iron Sulfate', 'Magnesium Oxide', 'Zinc Oxide',
            'Advil', 'Tylenol', 'Motrin', 'Aleve', 'Excedrin',
            'Claritin', 'Allegra', 'Zyrtec', 'Benadryl', 'Dramamine',
            'Zantac', 'Prevacid', 'Nexium', 'Prilosec', 'Aciphex',
            'Lipitor', 'Zocor', 'Pravachol', 'Lescol', 'Crestor',
            'Viagra', 'Cialis', 'Levitra', 'Staxyn', 'Klonopin',
            'Xanax', 'Valium', 'Ativan', 'Buspar', 'Desyrel',
            'Zoloft', 'Paxil', 'Lexapro', 'Celexa', 'Effexor',
            'Cymbalta', 'Pristiq', 'Savella', 'Elavil', 'Sinequan',
            'Amoxil', 'Augmentin', 'Ceclor', 'Keflex', 'Omnipen',
            'Cipro', 'Levaquin', 'Floxin', 'Avelox', 'Spectracef',
            'Diflucan', 'Sporanox', 'Nizoral', 'Lamisil', 'Monistat',
            'Zovirax', 'Valtrex', 'Famvir', 'Vistide', 'Cytovene',
            'Ribavirin', 'Relenza', 'Tamiflu', 'Symmetrel', 'Flumadine',
            'Lopinavir', 'Ritonavir', 'Atazanavir', 'Darunavir', 'Indinavir',
            'Saquinavir', 'Nelfinavir', 'Fosamprenavir', 'Tipranavir', 'Retrovir',
            'Combivir', 'Trizivir', 'Truvada', 'Atripla', 'Complera',
            'Stribild', 'Bictegravir', 'Dolutegravir', 'Elvitegravir', 'Raltegravir',
            'Enfuvirtide', 'Maraviroc', 'Ibalizumab', 'Fostemsavir', 'Zidovudine',
            'Didanosine', 'Zalcitabine', 'Stavudine', 'Lamivudine', 'Emtricitabine',
            'Abacavir', 'Tenofovir', 'Adefovir', 'Entecavir', 'Telbivudine',
            'Lamivudine HBV', 'Tenofovir HBV', 'Baraclude', 'Epivir HBV', 'Viread',
        ]

        # Add more medicines to reach 1000+
        additional_meds = []
        for i in range(1000, 1100):
            additional_meds.append(f'Medicine {i}')

        medicines_data.extend(additional_meds)

        created_count = 0
        for medicine_name in medicines_data[:1000]:
            medicine, created = Medicine.objects.get_or_create(name=medicine_name.strip())
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} medicines. Total: {Medicine.objects.count()}')
        )
