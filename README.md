# Pruebas automatizadas de Urban Routes
## _Sprint 8 / César Enrique Aburto Huerta - Cohorte 21_
## Paquetes necesarios

Se requieren los siguientes paquetes para correr las pruebas pytest y funciones selenium<br>
Asegurate de ubicarte en la carpeta del proyecto, puedes usar 'cd', antes de ejecutar los siguientes comandos.

- **Pytest:** utiliza la terminal para instalar el paquete correspondiente pytest. 
```sh
  pip install pytest
```
- **Requests:** instala este paquete con el mismo comando usando el nombre correspondiente del paquete 
```sh
  pip install requests
```
## Url de la solicitud
Antes de proceder con las pruebas asegurate de actualizar `urban_routes_url` en **data.py** con una Url activa del servidor de _TripleTen_.<br>
>El servidor puede detenerse después de un tiempo, es necesario volver a iniciar el servidor cuando esta situación se presente
## Correr las pruebas
- Ejecutar el comando `pytest` ideal para verificar rápidamente si las pruebas pasan o fallan, sin demasiados detalles adicionales.<br>
- El comando `pytest -v` "Verbose Mode" es ideal para depuración o escenarios en los que deseas un desglose detallado del estado de cada prueba.<br>
- Para ejecutar las pruebas con el botón "Run" asegurarse de hacerlo con la opción **Current File** seleccionando **main.py**<br>
también puede añadir una nueva configuración: **Edit configurations... > Add new configuration > Python test > pytest**
> Nota: Se hicieron ajustes en `setup_class`, la configuración por defecto presentaba errores
```python
    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)
        cls.driver.maximize_window()
        cls.routes_page = UrbanRoutesPage(cls.driver)
```
## Objetivo de las pruebas
Las pruebas automatizadas cubren el proceso completo de pedir un taxi.

- Configurar la dirección
- Seleccionar la tarifa Comfort.
- Rellenar el número de teléfono.
- Agregar una tarjeta de crédito.
- Escribir un mensaje para el controlador.
- Pedir una manta y pañuelos.
- Pedir 2 helados.
- Aparece el modal para buscar un taxi.
- Esperar a que aparezca la información del conductor en el modal

## Enfoque del código

Muchas de las pruebas están interrelacionadas, ya que comparten pasos complementarios necesarios para llegar al elemento deseado. <br>
Esto permite optimizar el código al evitar la repetición de métodos. Este enfoque resulta especialmente útil cuando identificamos <br>
que alcanzar un elemento requiere una secuencia específica de acciones que ya se encuentran en otras pruebas.<br>

Sin embargo, algunos métodos se implementaron de manera independiente, sin depender de otras pruebas. Esto se hizo para evitar que <br>
dichas pruebas sean completamente dependientes y puedan ejecutarse de manera autónoma cuando sea posible, garantizando mayor <br>
flexibilidad en el proceso de pruebas

## Estructura de las pruebas automatizadas en UrbanRoutes POM

Este proyecto utiliza la arquitectura **Page Object Model (POM)** para organizar y gestionar las pruebas automatizadas de UrbanRoutes, <br>
una plataforma enfocada en el pedido de servicios de transporte. A continuación, se describen los aspectos principales del código:

### Gestión del Driver

La clase `TestUrbanRoutes` incluye métodos para configurar y cerrar el navegador web mediante el uso de `setup_class` y `teardown_class`. <br>
Esto asegura que:

- El entorno de pruebas esté correctamente inicializado (por ejemplo, maximización de la ventana y configuración de capacidades del navegador).
- Los recursos se liberen al finalizar las pruebas.

### Pruebas del flujo funciona

Cada prueba automatizada verifica un aspecto específico del proceso de pedido de un taxi. Estas pruebas incluyen:

1. **Selección de Ruta** (test_set_route): Comprueba que la ruta seleccionada corresponda a las direcciones esperadas.
2. **Tarifa Comfort** (test_select_comfort_rate): Valida la selección de una tarifa específica, como "Comfort".
3. **Ingreso de Número Telefónico** (test_set_phone_number): Verifica que se pueda configurar correctamente un número de teléfono.
4. **Método de Pago** (test_set_card_method): Garantiza la adición exitosa de una tarjeta al método de pago.
5. **Mensaje al Conductor** (test_set_message_for_driver): Asegura que se pueda ingresar un mensaje personalizado para el conductor.
6. **Pedir una manta y pañuelos** (test_activate_blankets_and_hankies_switch): Comprueba que el switch está activo después de hacer clic en él.
7. **Pedido de Helados** (test_order_ice_cream): Valida que se sumaron 2 helados de diferente sabor.
8. **Validación del Modal de Confirmación** (test_modal_to_search_taxi_appears): Comprueba que el modal de búsqueda de taxi aparece al confirmar el viaje.
9. **Seguimiento del Conductor** (test_wait_info_driver): Verifica que el modal muestra la llegada del conductor.