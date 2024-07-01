import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# Crear objeto del controlador de Firefox
driver = webdriver.Firefox()


url = "https://desafiodataentryfront.vercel.app/"
driver.get(url)


download_dir = r'C:\\User\\Files\\Descargas'


wait = WebDriverWait(driver, 30)  # Esperar hasta 10 segundos

# Función para esperar a que las animaciones de Toastify se completen
def wait_for_toastify_completion():
    print("Esperando que aparezca 'Esto puede tardar unos minutos'...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Esto puede tardar unos minutos']")))
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//p[text()='Esto puede tardar unos minutos']")))
    print("'Esto puede tardar unos minutos' ha desaparecido.")
    
    print("Esperando que aparezca 'Lista de precios descargada con éxito'...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='alert']//div[text()='Lista de precios descargada con éxito']")))
    wait.until(EC.staleness_of(driver.find_element(By.XPATH, "//div[@role='alert']//div[text()='Lista de precios descargada con éxito']")))
    print("'Lista de precios descargada con éxito' ha desaparecido.")

try:
    # Localizar todos los botones por su etiqueta
    botones = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
    
    
    if len(botones) >= 3:
        
        botones[0].click()
        time.sleep(5)  
        
        
        segundo_boton = wait.until(EC.element_to_be_clickable((By.ID, "download-button-autofix")))
        segundo_boton.click()
        time.sleep(2)  

        # Esperar hasta que los campos de usuario y contraseña estén presentes
        usuario_campo = wait.until(EC.presence_of_element_located((By.ID, "username")))
        contraseña_campo = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        
        usuario_campo.send_keys("desafiodataentry")
        contraseña_campo.send_keys("desafiodataentrypass")

        # Hacer clic en el botón de inicio de sesión
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        time.sleep(5)  


        # Lista para almacenar los nombres de los labels
        marcas_repuestos = []

        # Iterar sobre los inputs desde 'marca-1' hasta 'marca-7'
        for i in range(1, 8):
            input_id = f"marca-{i}"
            label = wait.until(EC.presence_of_element_located((By.XPATH, f"//label[@for='{input_id}']")))
            nombre_label = label.text
            marcas_repuestos.append(nombre_label)

            marca_input = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
            marca_input.click()  # Marcar el input
            time.sleep(2)  

            # Hacer clic en el botón correspondiente después de marcar el input
            segundo_archivo_boton = wait.until(EC.element_to_be_clickable((By.ID, "download-button")))
            segundo_archivo_boton.click()
            time.sleep(2)  
            
            # Esperar a que las animaciones de Toastify se completen
            wait_for_toastify_completion()
            
            # Desmarcar el input
            marca_input.click()
            time.sleep(2)  


        # Guardar los nombres en un archivo txt
        with open(os.path.join(download_dir, 'marcas.txt'), 'w') as file:
            for nombre in marcas_repuestos:
                file.write(nombre + '\n')

        print(f"Nombres guardados en {os.path.join(download_dir, 'marcas.txt')}")

        # Hacer clic en el botón que despliega el menú de cierre de sesión
        desplegar_menu_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='button']")))
        desplegar_menu_button.click()
        time.sleep(2)  

        # Hacer clic en el botón de cerrar sesión
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Cerrar sesión']")))
        logout_button.click()
        time.sleep(5)  

        
        tercer_boton = wait.until(EC.element_to_be_clickable((By.ID, "download-button-mundo-repcar")))
        tercer_boton.click()
        time.sleep(2)

        # Esperar hasta que los campos de usuario y contraseña estén presentes nuevamente
        usuario_campo = wait.until(EC.presence_of_element_located((By.ID, "username")))
        contraseña_campo = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        # Ingresar el usuario y la contraseña nuevamente
        usuario_campo.send_keys("desafiodataentry")
        contraseña_campo.send_keys("desafiodataentrypass")

        # Hacer clic en el botón de inicio de sesión nuevamente
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        time.sleep(5)  # Esperar un tiempo para que la autenticación se complete y la página se cargue

        # Buscar y hacer clic en el botón con id "download-button"
        tercer_archivo_boton = wait.until(EC.element_to_be_clickable((By.ID, "download-button")))
        tercer_archivo_boton.click()
        time.sleep(4)  # Esperar un tiempo para asegurar que la descarga se complete
        
    else:
        print("No se encontraron los 3 botones esperados.")

finally:
    # Cerrar el navegador
    driver.quit()