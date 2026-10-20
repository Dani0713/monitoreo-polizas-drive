# Monitoreo y Sincronización de Pólizas en Google Drive

Proyecto desarrollado para la detección automatizada del ciclo de vida de pólizas en formato PDF dentro de una carpeta compartida en Google Drive.

* **Equipo:** Equipo 1 (CACHEtes team)
* **Enfoque:** Código Nativo en Servidor Propio (Python & Watcher/API)

---

## Descripción del Proyecto

El sistema implementa un mecanismo de monitoreo desatendido (polling) mediante la API oficial de Google Drive v3. A través de una máquina de estados y comparación de metadatos contra un registro en caché local (`estado_polizas.json`), el script identifica de manera precisa:

1. **Altas:** Carga de nuevas pólizas PDF en la carpeta.
2. **Modificaciones (Updates):** Cambios en el archivo detectados por variaciones en la marca temporal (`modifiedTime`) o suma de verificación (`md5Checksum`).
3. **Bajas:** Pólizas eliminadas o enviadas a la papelera (`trashed = true`).

---

## Tecnologías y Librerías Utilizadas

* **Python 3.10+** (Probado en Python 3.13)
* **`google-api-python-client`**: SDK oficial para interactuar con los endpoints de Google Drive API v3 (`files.list`).
* **`google-auth` / `google-auth-oauthlib`**: Manejo de autenticación máquina a máquina mediante Cuentas de Servicio (Service Account) sin intervención interactiva de navegador.
* **`json` y `os`**: Librerías estándar de Python para resolución de rutas dinámicas y persistencia del estado en caché local.

---

## Requisitos Previos y Configuración

### 1. Google Cloud Platform (GCP)

1. Habilitar la **Google Drive API** dentro de un proyecto en Google Cloud Console.
2. Crear una **Cuenta de Servicio (Service Account)** y generar una clave privada en formato JSON.
3. Descargar el archivo de clave y guardarlo en la raíz de este proyecto con el nombre `credentials.json`.
4. Compartir la carpeta de Google Drive donde se alojan las pólizas con el correo de la Service Account (con permisos de *Lector* o *Editor*).

### 2. Configuración del Entorno Local

1. Clonar el repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
