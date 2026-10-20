import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configuración
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')
ESTADO_CACHE_FILE = os.path.join(BASE_DIR, 'estado_polizas.json')
FOLDER_ID = '1ji5xsGV6cojdazW8HvgI12BS5RYsQcHT'  # Tu ID de carpeta

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def cargar_estado_anterior():
    if os.path.exists(ESTADO_CACHE_FILE):
        with open(ESTADO_CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_estado_actual(estado):
    with open(ESTADO_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=4)

def obtener_archivos_actuales(service):
    """Obtiene los archivos PDF dentro de la carpeta seleccionada."""
    query = f"'{FOLDER_ID}' in parents and trashed = false and mimeType = 'application/pdf'"
    results = service.files().list(
        q=query, 
        fields="files(id, name, modifiedTime, md5Checksum)"
    ).execute()
    
    # Lo convertimos a un diccionario {id: {datos}}
    archivos_dict = {}
    for item in results.get('files', []):
        archivos_dict[item['id']] = {
            'name': item['name'],
            'modifiedTime': item['modifiedTime'],
            'md5Checksum': item.get('md5Checksum', '')
        }
    return archivos_dict

def detectar_cambios():
    service = get_drive_service()
    estado_previo = cargar_estado_anterior()
    archivos_actuales = obtener_archivos_actuales(service)

    nuevos = []
    modificados = []
    eliminados = []

    # 1. Detectar archivos nuevos y modificados
    for file_id, datos in archivos_actuales.items():
        if file_id not in estado_previo:
            nuevos.append(datos['name'])
        else:
            # Si cambió la fecha de modificación o el hash del contenido
            if datos['modifiedTime'] != estado_previo[file_id]['modifiedTime']:
                modificados.append(datos['name'])

    # 2. Detectar archivos eliminados (estaban antes pero ya no existen en Drive)
    for file_id, datos in estado_previo.items():
        if file_id not in archivos_actuales:
            eliminados.append(datos['name'])

    # 3. Mostrar reporte en consola
    print("=== REPORTE DE SINCRONIZACIÓN DE PÓLIZAS ===")
    if not nuevos and not modificados and not eliminados:
        print("Sin cambios detectados en la carpeta.")
    else:
        if nuevos:
            print("\n[NUEVAS PÓLIZAS CARGADAS]:")
            for nombre in nuevos:
                print(f"  + {nombre}")
        
        if modificados:
            print("\n[PÓLIZAS ACTUALIZADAS / UPDATES]:")
            for nombre in modificados:
                print(f"  * {nombre}")
                
        if eliminados:
            print("\n[PÓLIZAS ELIMINADAS]:")
            for nombre in eliminados:
                print(f"  - {nombre}")

    # Guardar el estado actual como la nueva base de comparación
    guardar_estado_actual(archivos_actuales)

if __name__ == '__main__':
    detectar_cambios()