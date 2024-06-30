from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import AutomateBrowser.constants as const
import time
import os
import logging


# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutomateDownloads(webdriver.Chrome):
    def __init__(self, download_path=r"./Files", teardown=True):
        self.download_path = os.path.abspath(download_path)
        self.driver_path = const.DRIVER_PATH
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + self.driver_path

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        # Establecer ruta de descarga
        prefs = {"download.default_directory": self.download_path}
        options.add_experimental_option("prefs", prefs)

        super(AutomateDownloads, self).__init__(options=options)
        logger.info("Inicialización de WebDriver completada.")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
            logger.info("Cierre del WebDriver completado.")

    def land_first_page(self):
        try:
            self.get(const.BASE_URL)
            logger.info(f"Cargada la página inicial: {const.BASE_URL}")
        except Exception as e:
            logger.error(f"Error al cargar la página web: {e}")

    def login_page(self):
        try:
            username = self.find_element(By.ID, "username")
            username.send_keys(const.USERNAME)
            logger.info("Nombre de usuario ingresado.")

            password = self.find_element(By.ID, "password")
            password.send_keys(const.PASSWORD)
            logger.info("Contraseña ingresada.")

            login = self.find_element(By.ID, "login-button")
            login.click()
            logger.info("Click en el botón de inicio de sesión.")
        except Exception as e:
            logger.error(f"Error en la página de inicio de sesión: {e}")

    def autorepuestos_list(self):
        self.land_first_page()
        try:
            autorepuestos_element = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, "download-button-autorepuestos-express"))
            )
            autorepuestos_element.click()
            logger.info("Click en el botón de descarga de AutoRepuestos Express.")
            logger.info("Esperando 20 segundos para la descarga...")
            time.sleep(20)
        except TimeoutException as e:
            logger.error(f"Error al cargar el botón de descarga de AutoRepuestos Express: {e}")

    def autofix_list(self):
        self.land_first_page()
        try:
            autofix_element = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, "download-button-autofix"))
            )
            autofix_element.click()
            logger.info("Click en el botón de descarga de AutoFix.")
            logger.info("Esperando 10 segundos para la descarga...")
            time.sleep(10)
        except TimeoutException as e:
            logger.error(f"Error al cargar el botón de descarga de AutoFix: {e}")

        if self.current_url == const.LOGIN_URL:
            self.login_page()

        # Almacena el Id de todas las marcas de repuestos
        element_ids = [f"marca-{i}" for i in range(1, 8)]

        # Selecciona todas las marcas de repuestos
        for element_id in element_ids:
            try:
                # Espera hasta que el elemento este presente en la pagina y lo guarda en variable
                element = WebDriverWait(self, 10).until(
                    EC.presence_of_element_located((By.ID, element_id))
                )
                element.click()
                logger.info(f"Click en el elemento con ID {element_id}.")
            except Exception as e:
                logger.error(f"No se pudo encontrar el elemento con ID {element_id}: {e}")

        download_button = self.find_element(By.ID, "download-button")
        download_button.click()
        logger.info("Click en el botón de descarga final.")

        try:
            WebDriverWait(self, 180).until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "div[role='alert'].Toastify__toast-body"),
                    "Lista de precios descargada con éxito"
                )
            )
            logger.info("Lista de precios descargada con éxito.")
        except Exception as e:
            logger.error(f"El mensaje de éxito de la descarga no apareció: {e}")

    def mundo_repcar_list(self):
        self.land_first_page()
        try:
            mundo_repcar_element = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, "download-button-mundo-repcar"))
            )
            mundo_repcar_element.click()
            logger.info("Click en el botón de descarga de Mundo RepCar.")
            logger.info("Esperando 10 segundos para la descarga...")
            time.sleep(10)
        except TimeoutException as e:
            logger.error(f"Error al cargar el botón de descarga de Mundo RepCar: {e}")

        if self.current_url == const.LOGIN_URL:
            self.login_page()

        try:
            download_list = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, "download-link"))
            )
            download_list.click()
            logger.info("Click en el enlace de descarga de la lista.")
            logger.info("Esperando 20 segundos para la descarga...")
            time.sleep(20)
        except Exception as e:
            logger.error(f"Error al cargar el enlace de descarga: {e}")