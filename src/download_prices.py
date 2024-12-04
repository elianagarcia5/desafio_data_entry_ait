import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def move_downloaded_file(name_file, file_extension):
    default_download_dir = 'C:\\Users\\nCuello\\Downloads'
    downloaded_files = 'C:\\Users\\nCuello\\Desktop\\AIT solutions\\desafio_data_entry_ait\\data\\downloaded_files'

    if not os.path.exists(downloaded_files):
        os.makedirs(downloaded_files)

    max_wait_time = 60
    wait_interval = 5
    elapsed_time = 0

    while elapsed_time < max_wait_time:
        files = os.listdir(default_download_dir)
        downloaded_files_list = [f for f in files if f.startswith(name_file) and f.endswith(file_extension)]

        if downloaded_files_list:
            # Generar nombre para el archivo según proveedor
            
            filename = f"{name_file}{file_extension}"
            source_path = os.path.join(default_download_dir, downloaded_files_list[0])
            destination_path = os.path.join(downloaded_files, filename)
            try:
                os.replace(source_path, destination_path)
                print(f"Archivo movido a: {destination_path}")
                return
            except Exception as e:
                print(f"Error al mover el archivo: {e}")
                return
        else:
            time.sleep(wait_interval)
            elapsed_time += wait_interval

    print(f"No se encontró ningún archivo descargado con el nombre '{name_file}{file_extension}'.")

def download_prices():
    chromedriver_path = 'C:\\Users\\nCuello\\Desktop\\Prueba técnica AIT\\src\\drivers\\chromedriver.exe'
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        url = 'https://desafiodataentryfront.vercel.app/'
        driver.get(url)

        key = driver.execute_script('return localStorage.getItem("your_localstorage_key");')

        if not key:
            button_login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="download-button-mundo-repcar"]')))
            button_login.click()
            username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
            username.send_keys('desafiodataentry')
            password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
            password.send_keys('desafiodataentrypass')
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[id='login-button']")))
            button.click()
            driver.get('https://desafiodataentryfront.vercel.app/')

        name_file = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[@id="provider-name-autorepuestos-express"]'))).text
        print(f"Nombre del archivo encontrado: {name_file}")
        download_button_xpath = f'//button[@id="download-button-{name_file.lower().replace(" ", "-")}"]'
        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, download_button_xpath)))

        download_button.click()

        time.sleep(5)
        file_extension = '.xlsx'
        move_downloaded_file(name_file, file_extension)
        
        url_mundoRepCar = 'https://res.cloudinary.com/ddbvsytpr/raw/upload/v1719274818/AutoRepuestos%20Express%20Lista%20de%20Precios.csv'
        response = requests.get(url_mundoRepCar)
        if response.status_code == 200:
            filename = "MundoRepCar.csv"
            # Ruta de guardado para el archivo
            downloads_path = os.path.join("C:\\Users\\nCuello\\Downloads", filename)

            # Guarda el archivo en la ruta establecida
            os.makedirs(os.path.dirname(downloads_path), exist_ok=True)
            with open(downloads_path, "wb") as file:
                file.write(response.content)
            print(f"Archivo descargado y guardado como {downloads_path}")
        else:
            print(f"Error en la solicitud: {response.status_code}")
        file_extension = '.csv'
        move_downloaded_file('MundoRepCar',file_extension)

        url_autofix = 'https://desafio.somosait.com/api/download?marcas=CH&marcas=VW&marcas=FI&marcas=CI&marcas=TY&marcas=FO&marcas=RN'
        response = requests.get(url_autofix)
        if response.status_code == 200:
            filename = "Autofix.xlsx"
            # Ruta donde guardar el archivo en un principio localmente
            downloads_path = os.path.join("C:\\Users\\nCuello\\Downloads", filename)

            # Guarda el archivo en la ruta del escritorio
            os.makedirs(os.path.dirname(downloads_path), exist_ok=True)
            with open(downloads_path, "wb") as file:
                file.write(response.content)
            print(f"Archivo descargado y guardado como {downloads_path}")
        else:
            print(f"Error en la solicitud: {response.status_code}")
        file_extension = '.xlsx'
        move_downloaded_file('Autofix',file_extension)
    finally:
        driver.quit()

if __name__ == "__main__":
    download_prices()
