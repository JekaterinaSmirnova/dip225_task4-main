import csv
import zlib
import openpyxl

# Funkcija, lai ģenerētu CRC32 kodējumu
def generate_crc32(full_name):
    return format(zlib.crc32(full_name.encode('utf-8')) & 0xFFFFFFFF, '08x')

# 1. Lasīt people.csv un sagatavot sarakstu ar pilnajiem vārdiem
people_file = 'people.csv'
full_names = []

try:
    with open(people_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Izlaist galveni, ja tāda ir
        for row in reader:
            full_name = row[0].strip()  # Pieņemts, ka pilnais vārds ir pirmajā kolonnā
            full_names.append(full_name)
except FileNotFoundError:
    print(f"Fails {people_file} nav atrasts.")
    exit()

# 2. Ģenerēt CRC32 kodējumu katram pilnajam vārdam
crc32_names = {full_name: generate_crc32(full_name) for full_name in full_names}

# 3. Lasīt salary.xlsx un atrast algas
salary_file = 'salary.xlsx'
alga_dati = {}

try:
    wb = openpyxl.load_workbook(salary_file)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):  # Sākt no 2. rindas, pieņemot, ka 1. ir galvene
        encoded_name = row[0]  # Kodētais pilnais vārds
        salary = row[1]  # Alga
        if isinstance(salary, (int, float)):  # Pārbauda, vai alga ir skaitlis
            if encoded_name in alga_dati:
                alga_dati[encoded_name] += salary
            else:
                alga_dati[encoded_name] = salary
except FileNotFoundError:
    print(f"Fails {salary_file} nav atrasts.")
    exit()
except Exception as e:
    print(f"Radās kļūda: {e}")
    exit()



# 5. Identificēt algas tikai norādītajiem darbiniekiem
specific_employees = ["Adrienne Lambert", "Jo Rivers", "Hunter Hahn", "Chloe Ramirez"]
specific_salaries = {}

for employee in specific_employees:
    encoded_name = generate_crc32(employee)
    if encoded_name in alga_dati:
        salary = alga_dati[encoded_name]
        specific_salaries[employee] = salary
        print(f"Darbinieka {employee} kopējā alga ir: {salary}")
    else:
        print(f"Alga darbiniekam {employee} (kodēts: {encoded_name}) nav atrasta.")

