# WEB-SCRAPING-AMAZON

## Proyecto Web Scraping con Selenium para Amazon

Este proyecto utiliza **Selenium** y **Python** para realizar un scraping de productos desde la plataforma de comercio electrónico **Amazon**. Se extraen datos como el nombre, precio, y otros atributos de los productos listados, y se almacenan en un archivo **CSV**.

## Descripción

El script automatiza la navegación en Amazon para extraer información sobre los productos. Usando **Selenium**, el proyecto interactúa con el navegador web para obtener los datos, y luego los guarda en un archivo **CSV** que puede ser usado para análisis posteriores. El archivo **CSV** contiene información sobre los productos como su nombre, precio, enlace, etc.

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación para la automatización y extracción de datos.
- **Selenium**: Librería que permite controlar un navegador web para realizar el scraping.
- **Pandas**: Para almacenar los datos extraídos en un archivo **CSV**.
- **ChromeDriver**: Para controlar el navegador Google Chrome con Selenium.

## Instalación

### 1. Clona este repositorio:

```bash
git clone https://github.com/paezdev/web-scraping-amazon-selenium.git
```

### 2. Crea un entorno virtual:

#### Windows:
```bash
python -m venv .venv
```

#### Linux/Mac:
```bash
python3 -m venv .venv
```

### 3. Activa el entorno virtual:

#### Windows:
```bash
.venv\Scripts\activate
```

#### Linux/Mac:
```bash
source .venv/bin/activate
```

### 4. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, puedes instalar las dependencias manualmente:

```bash
pip install selenium pandas webdriver-manager
```

### 5. Configura **ChromeDriver**:

- Descarga **ChromeDriver** desde [aquí](https://sites.google.com/chromium.org/driver/).
- Asegúrate de que la versión del **ChromeDriver** coincida con la de tu navegador **Google Chrome**.
- Coloca el archivo **chromedriver** en la misma carpeta que el script o en una ubicación que esté en el **PATH** del sistema.

## Uso

### 1. Ejecuta el script de scraping:

Una vez que hayas configurado el entorno y las dependencias, ejecuta el siguiente comando para iniciar el scraping:

```bash
python PáezRamírez_JeanCarlos_Analizando_EA1.py
```

### 2. Resultado

El script navegará por Amazon y extraerá los datos de los productos. Los datos serán guardados en un archivo **output.csv** en el directorio donde ejecutaste el script.

El archivo **output.csv** tendrá la siguiente estructura de columnas:

- **Nombre del Producto**
- **Precio**

## Estructura del Proyecto

La estructura de carpetas y archivos del proyecto es la siguiente:

```
web-scraping-amazon-selenium/
│
├── .venv/                  # Entorno virtual para gestionar dependencias
├── PáezRamírez_JeanCarlos_Analizando_EA1.py      # Script principal que realiza el scraping de Amazon
├── output.csv              # Archivo CSV con los datos extraídos de Amazon
├── requirements.txt        # Archivo con las dependencias del proyecto
├── .gitignore              # Archivos y carpetas que deben ser ignorados por git
└── README.md               # Este archivo
```

## Detalles sobre el Código

### PáezRamírez_JeanCarlos_Analizando_EA1.py

El archivo `PáezRamírez_JeanCarlos_Analizando_EA1.py` es el corazón del proyecto. A continuación, se describe brevemente su funcionamiento:

1. **Importación de librerías**:
   Se importan las librerías necesarias para la automatización (Selenium) y el manejo de datos (Pandas).
   
2. **Configuración de WebDriver**:
   Se configura el **WebDriver** de **Chrome** para usar Selenium. Este WebDriver es el que controla el navegador durante la ejecución del script.

3. **Extracción de Datos**:
   El script navega por las páginas de Amazon y extrae datos específicos de los productos. Esto incluye el nombre del producto, precio, descripción, y enlace a la página del producto.

4. **Almacenamiento de Datos**:
   Los datos extraídos se almacenan en un archivo **output.csv** utilizando la librería **Pandas**. Si hay varios productos, estos se irán agregando al archivo.

### Proceso de Scraping

El scraping se realiza siguiendo estos pasos:

1. **Acceso a Amazon**:
   El script abre el navegador y navega por la página de Amazon.

2. **Interacción con la página**:
   Se simula el desplazamiento por la página para cargar más productos.

3. **Extracción de productos**:
   Se extraen los datos relevantes de cada producto utilizando la estructura HTML de la página.

4. **Almacenamiento**:
   Los datos se guardan en un archivo **CSV** para su análisis posterior.

## Contribuciones

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un **fork** de este repositorio.
2. Crea una nueva rama para tus cambios (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios y haz un **commit** (`git commit -am 'Añadir nueva característica'`).
4. Haz un **push** a tu rama (`git push origin feature/nueva-caracteristica`).
5. Abre un **Pull Request** con una descripción detallada de tus cambios.

## Licencia

Este proyecto está bajo la Licencia **MIT**. Para más detalles, consulta el archivo `LICENSE`.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto:

- **GitHub**: [paezdev](https://github.com/paezdev)
- **Correo electrónico**: [paezdev@gmail.com](mailto:paezdev@gmail.com)