# Transcriptor de Video a Texto con Google Cloud

Este proyecto es una herramienta de línea de comandos en Python que automatiza la transcripción de archivos de video. Utiliza la API de Google Cloud Speech-to-Text para generar transcripciones de alta precisión.

## Características

-   **Extracción de Audio:** Extrae automáticamente la pista de audio de archivos de video (MP4, MOV, etc.).
-   **Integración con Google Cloud:** Sube de forma segura los archivos de audio a Google Cloud Storage para su procesamiento.
-   **Transcripción Asíncrona:** Utiliza el modo de reconocimiento de larga duración de la API de Speech-to-Text, ideal para videos largos.
-   **Organización de Archivos:** Guarda los archivos de audio (`.mp3`) y las transcripciones (`.txt`) en una carpeta de salida (`outputs/`) para mantener el proyecto ordenado.
-   **Configuración Segura:** Gestiona las claves de API y la configuración del proyecto de forma segura a través de un archivo `.env`.

## Estructura del Proyecto

```
app-transcripcion-videos/
├── .git/
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── requirements.txt
├── transcripcion.py
├── outputs/
├── secrets/
└── videos/
```

## Prerrequisitos

Antes de empezar, asegúrate de tener lo siguiente:

1.  **Python 3.7+**
2.  **FFmpeg:** Es una dependencia de `moviepy` para la manipulación de video y audio.
    -   **Windows:** `choco install ffmpeg`
    -   **macOS:** `brew install ffmpeg`
    -   **Linux:** `sudo apt-get install ffmpeg`
3.  **Cuenta de Google Cloud:**
    -   Un proyecto de GCP activo.
    -   La API de **Speech-to-Text** habilitada.
    -   Un **Bucket** de Google Cloud Storage creado.
    -   Una **cuenta de servicio** con permisos para acceder a Storage y Speech-to-Text. Deberás descargar la clave de esta cuenta en formato JSON.

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

**1. Clona el repositorio:**
```bash
git clone <URL_DEL_REPOSITORIO_EN_GITHUB>
cd video-transcription-gcp
```

**2. Crea y activa un entorno virtual:**
```bash
# Crear el entorno
python -m venv .venv

# Activar en Windows
.venv\Scripts\activate

# Activar en macOS/Linux
source .venv/bin/activate
```

**3. Instala las dependencias:**
```bash
pip install -r requirements.txt
```

**4. Configura tus credenciales de Google Cloud:**
-   Coloca el **archivo JSON** de tu cuenta de servicio dentro de la carpeta `secrets/`.
-   Establece la variable de entorno `GOOGLE_APPLICATION_CREDENTIALS` para que apunte a tu clave. En PowerShell (Windows):
    ```powershell
    $env:GOOGLE_APPLICATION_CREDENTIALS = ".\secrets\tu-archivo-json.json"
    ```
    *Nota: Este comando solo establece la variable para la sesión actual de la terminal.*

**5. Configura las variables del proyecto:**
-   Crea una copia del archivo `.env.example` y renómbrala a `.env`.
-   Abre el archivo `.env` y rellena los valores con la información de tu proyecto de Google Cloud:
    ```dotenv
    GCP_PROJECT_ID="tu-gcp-project-id"
    GCS_BUCKET_NAME="tu-gcs-bucket-name"
    AUDIO_LANGUAGE_CODE="es-CL"
    ```

## Uso

Para transcribir un video, ejecuta el script `transcripcion.py` desde la raíz del proyecto, pasándole la ruta al archivo de video como argumento.

```bash
python transcripcion.py "ruta/al/video.mp4"
```

Por ejemplo, si tienes tus videos en la carpeta `videos/`:
```bash
python transcripcion.py "videos/mi-conferencia.mp4"
```

La transcripción final se guardará en la carpeta `outputs/` con el mismo nombre que el video, pero con la extensión `.txt`.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar, por favor abre un **issue** o envía un **pull request** con tus mejoras o correcciones.
## Contacto
Para cualquier duda o consulta, puedes contactarme a través de mi perfil de GitHub o abrir un issue en este repositorio.
```
## Créditos
Este proyecto fue desarrollado por [Tu Nombre o Tu Organización] como parte de un ejercicio de aprendizaje y automatización de tareas con Python y Google Cloud.

## Agradecimientos
Agradecimientos especiales a la comunidad de desarrolladores de Python y a Google Cloud por proporcionar herramientas tan poderosas y accesibles para la transcripción de audio y video.
```
## Notas Adicionales
-   Asegúrate de que el archivo de video esté en un formato compatible (MP4, MOV, etc.).
-   La transcripción puede tardar un tiempo dependiendo de la duración del video y la carga actual de la API de Google Cloud.
-   Revisa los límites de uso de la API de Google Cloud para evitar costos inesperados. Puedes encontrar más información en la [documentación oficial de Google Cloud](https://cloud.google.com/speech-to-text/pricing).