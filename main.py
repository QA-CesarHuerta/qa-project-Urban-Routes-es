import time

from selenium.webdriver.ie.service import Service

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_rate_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    tcard_active = (By.XPATH, "//div[contains(@class, 'tcard active')]//div[@class='tcard-title' and text()='Comfort']")
    phone_number_add_button = (By.CLASS_NAME, "np-button")
    phone_number_field = (By.ID, "phone")
    phone_number_continue_button = (By.XPATH, "//button[@class='button full' and text()='Siguiente']")
    phone_number_code_field = (By.ID, "code")
    confirm_phone_number_code_button = (By.XPATH, "//button[@class='button full' and text()='Confirmar']")
    payment_method_add_button = (By.CLASS_NAME, "pp-button")
    card_add_row = (By.CSS_SELECTOR, ".pp-row.disabled")
    card_number_field = (By.ID, "number")
    card_code_field = (By.XPATH, "//div[@class='card-second-row']//input")
    card_add_confirm_button = (By.XPATH, "//button[@class='button full' and text()='Agregar']")
    card_close_button_no_unusual = (By.XPATH, "//div[contains(@class, 'payment-picker')]//div[contains(@class, 'section') and not(contains(@class, 'unusual'))]//button[contains(@class, 'close-button')]")
    message_for_driver_field = (By.XPATH, "//input[@placeholder='Traiga un aperitivo']")
    blankets_and_hankies_switch = (By.XPATH, "//div[@class='r-sw-container' and .//div[contains(text(), 'Manta y pañuelos')]]")
    ice_cream_standard =(By.XPATH, "//div[@class='r-counter-container' and .//div[contains(text(), 'Helado')]]")
    ice_cream_chocolate = (By.XPATH, "//div[@class='r-counter-container' and .//div[contains(text(), 'Chocolate')]]")
    confirm_traveling_button = (By.CLASS_NAME, "smart-button")
    modal_search_taxi = (By.CLASS_NAME, "order-body")
    modal_search_taxi_title = (By.CLASS_NAME, "order-header-title")
    modal_search_taxi_time = (By.CLASS_NAME, "order-header-time")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self):
        self.set_from(data.address_from)
        self.set_to(data.address_to)

    def click_on_request_taxi_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        ).click()

    def click_on_comfort_icon(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.comfort_rate_icon)
        ).click()

    def get_tcard_active_text(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.tcard_active)
        ).text

    def select_comfort_rate(self):
        self.set_route()
        self.click_on_request_taxi_button()
        self.click_on_comfort_icon()

    def get_text_on_add_phone_button(self):
        np_button_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.phone_number_add_button))
        np_text_element = np_button_element.find_element(By.CLASS_NAME, "np-text")
        return np_text_element.text

    def click_on_add_phone_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.phone_number_add_button)
        ).click()

    def set_phone_number_field(self, phone_number):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.phone_number_field)
        ).send_keys(phone_number)

    def click_on_continue_phone_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.phone_number_continue_button)
        ).click()

    def set_phone_code_field(self, phone_code):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.phone_number_code_field)
        ).send_keys(phone_code)

    def click_on_confirm_phone_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.confirm_phone_number_code_button)
        ).click()

    def set_phone_number(self, phone_number, retrieve_code_func):
        self.click_on_add_phone_button()
        self.set_phone_number_field(phone_number)
        self.click_on_continue_phone_button()
        phone_code = retrieve_code_func(self.driver)
        if phone_code is None:
            print("Error: El código de confirmación no fue generado.")
        self.set_phone_code_field(phone_code)
        self.click_on_confirm_phone_button()

    def click_payment_method_add_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.payment_method_add_button)
        ).click()

    def click_card_add_row(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.card_add_row)
        ).click()

    def set_card_number_field(self, card_number):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.card_number_field)
        ).send_keys(card_number)

    def set_card_code_field(self, card_code):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.card_code_field)
        ).send_keys(card_code, Keys.TAB)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='head' and text()='Agregar tarjeta']"))
        ).click()

    def click_card_add_confirm_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.card_add_confirm_button)
        ).click()

    def click_card_close_button_no_unusual(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.card_close_button_no_unusual)
        ).click()

    def set_payment_method(self, card_number, card_code):
        self.click_payment_method_add_button()
        self.click_card_add_row()
        self.set_card_number_field(card_number)
        self.set_card_code_field(card_code)
        self.click_card_add_confirm_button()
        self.click_card_close_button_no_unusual()

    def set_message_for_driver_field(self, message):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.message_for_driver_field)
        ).send_keys(message)

    def activate_blankets_and_hankies_switch(self):
        scroll_target = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.blankets_and_hankies_switch)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", scroll_target)
        time.sleep(.5)
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='r-sw-container']//span[@class='slider round']"))
        ).click()

    def increment_ice_cream_standard(self):
        scroll_target = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.ice_cream_standard)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", scroll_target)
        time.sleep(.5)
        self.driver.find_element(*self.ice_cream_standard).find_element(By.XPATH, ".//div[@class='counter-plus']").click()

    def increment_ice_cream_chocolate(self):
        scroll_target = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.ice_cream_chocolate)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", scroll_target)
        time.sleep(.5)
        self.driver.find_element(*self.ice_cream_chocolate).find_element(By.XPATH, ".//div[@class='counter-plus']").click()

    def set_two_ice_cream(self):
        self.increment_ice_cream_standard()
        self.increment_ice_cream_chocolate()

    def click_on_confirm_traveling_button(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.confirm_traveling_button)
        ).click()

    def get_modal_search_taxi_body(self):
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.modal_search_taxi))


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)
        cls.driver.maximize_window()
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page.set_route()
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    def test_select_comfort_rate(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page.select_comfort_rate()
        assert self.routes_page.get_tcard_active_text() == "Comfort"

    def test_set_phone_number(self):
        self.test_select_comfort_rate()
        self.routes_page.set_phone_number(data.phone_number, retrieve_phone_code)
        assert self.routes_page.get_text_on_add_phone_button() == data.phone_number

    def test_set_card_method(self):
        self.test_select_comfort_rate()
        self.routes_page.set_payment_method(data.card_number, data.card_code)
        payment_value_text = self.driver.find_element(By.CLASS_NAME, "pp-value-text").text
        assert payment_value_text == "Tarjeta", f"El texto encontrado fue: {payment_value_text}"

    def test_set_message_for_driver(self):
        self.test_select_comfort_rate()
        self.routes_page.set_message_for_driver_field(data.message_for_driver)
        message_field_value = self.driver.find_element(By.XPATH, "//input[@placeholder='Traiga un aperitivo']").get_attribute("value")
        assert message_field_value == data.message_for_driver, f"El valor encontrado fue: {message_field_value}"

    def test_activate_blankets_and_hankies_switch(self):
        self.test_select_comfort_rate()
        self.routes_page.activate_blankets_and_hankies_switch()
        switch_status = self.driver.find_element(By.XPATH, "//div[@class='r-sw-container']//input[@type='checkbox']").is_selected()
        assert switch_status, "El switch no está activado correctamente"

    def test_order_ice_cream(self):
        self.test_select_comfort_rate()
        self.routes_page.set_two_ice_cream()
        standard_count = self.driver.find_element(*self.routes_page.ice_cream_standard).find_element(By.XPATH, ".//div[@class='counter-value']").text
        chocolate_count = self.driver.find_element(*self.routes_page.ice_cream_chocolate).find_element(By.XPATH, ".//div[@class='counter-value']").text
        assert standard_count == "1", f"El contador de helado estándar muestra: {standard_count}"
        assert chocolate_count == "1", f"El contador de helado chocolate muestra: {chocolate_count}"

    def test_modal_to_search_taxi_appears(self):
        self.test_select_comfort_rate()
        self.routes_page.set_phone_number(data.phone_number, retrieve_phone_code)
        self.routes_page.set_payment_method(data.card_number, data.card_code)
        self.routes_page.set_message_for_driver_field(data.message_for_driver)
        self.routes_page.click_on_confirm_traveling_button()
        modal_body = self.routes_page.get_modal_search_taxi_body()
        assert modal_body.is_displayed(), "El modal de búsqueda de taxi no apareció."

    def test_wait_info_driver(self):
        self.test_modal_to_search_taxi_appears()
        WebDriverWait(self.driver, 100).until(
            EC.text_to_be_present_in_element(self.routes_page.modal_search_taxi_title, "El conductor llegará"))
        final_title = self.driver.find_element(*self.routes_page.modal_search_taxi_title).text
        assert "El conductor llegará" in final_title, f"El título del modal muestra: {final_title}"

    @classmethod
    def teardown_class(cls):
        time.sleep(3)
        cls.driver.quit()