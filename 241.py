from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import zlib

# Funkcija, lai ģenerētu CRC32 kodējumu
def generate_crc32(full_name):
    return format(zlib.crc32(full_name.encode('utf-8')) & 0xFFFFFFFF, '08x')

# Specifiskie darbinieki
specific_employees = ["Adrienne Lambert", "Jo Rivers", "Hunter Hahn", "Chloe Ramirez"]

# Uzstādīt WebDriver
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Aizstāj ar savu ceļu uz ChromeDriver

# Atvērt tīmekļa lapu
driver.get('http://example.com')  # Šeit ievieto īsto URL, kur var meklēt darbinieku vārdus

# Sagatavot datus
specific_salaries = {}

# Meklēt katram darbiniekam un iegūt informāciju
for employee in specific_employees:
    encoded_name = generate_crc32(employee)
    try:
        # Atrodam meklēšanas lodziņu un ievadam darbinieka vārdu
        search_box = driver.find_element(By.NAME, 'search')  # Aizstāj ar pareizo elementa ID/klasi
        search_box.clear()
        search_box.send_keys(employee)
        search_box.send_keys(Keys.RETURN)

        # Pagaidām, līdz rezultāts tiek parādīts (varētu būt arī jāizmanto WebDriverWait)
        driver.implicitly_wait(5)

        # Iegūstam algu informāciju no lapas (aizstāj ar pareizo selektoru)
        salary_element = driver.find_element(By.XPATH, '//*[@id="salary"]')  # Aizstāj ar īsto XPATH

        # Pārliecināties, ka alga ir atrasta un iegūstam tās vērtību
        if salary_element:
            salary = salary_element.text
            specific_salaries[employee] = salary
            print(f"Darbinieka {employee} kopējā alga ir: {salary}")
        else:
            print(f"Alga darbiniekam {employee} nav atrasta.")
    except Exception as e:
        print(f"Kļūda meklējot darbinieku {employee}: {e}")

# Izvadīt norādīto darbinieku algas
print("Norādīto darbinieku algas:")
for name, salary in specific_salaries.items():
    print(f"Darbinieks: {name}, Alga: {salary}")

# Aizver pārlūkprogrammu
driver.quit()
