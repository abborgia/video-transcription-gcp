# -*- coding: utf-8 -*-
import os
import sys
from google.cloud import speech
from google.cloud import storage
from moviepy.editor import AudioFileClip, VideoFileClip
import time

# --- CONFIGURACIÓN ---
def load_dotenv(dotenv_path='.env'):
    """Carga variables de un archivo .env al entorno de ejecución."""
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    os.environ.setdefault(key, value)

# Cargar variables de entorno desde .env
load_dotenv()

# Lee la configuración desde las variables de entorno
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
AUDIO_LANGUAGE_CODE = os.getenv("AUDIO_LANGUAGE_CODE")

# Validar que las variables necesarias estén cargadas
if not all([GCP_PROJECT_ID, GCS_BUCKET_NAME, AUDIO_LANGUAGE_CODE]):
    print("Error: Faltan variables de configuración en el archivo .env o en el entorno.")
    print("Asegúrate de que GCP_PROJECT_ID, GCS_BUCKET_NAME y AUDIO_LANGUAGE_CODE estén definidos.")
    sys.exit(1)
# ---------------------

def extraer_audio(video_path):
    """
    Extrae el audio de un archivo de video y lo guarda como MP3 en la carpeta outputs.
    Retorna la ruta del archivo de audio creado.
    """
    print(f"1. Extrayendo audio del video: {video_path}")
    try:
        video = VideoFileClip(video_path)
        base_name = os.path.basename(video_path)
        audio_filename = os.path.splitext(base_name)[0] + ".mp3"
        audio_path = os.path.join("outputs", audio_filename)
        video.audio.write_audiofile(audio_path)
        video.close()
        print(f"   -> Audio guardado en: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"   -> Error al extraer el audio: {e}")
        return None

def subir_a_gcs(file_path, bucket_name):
    """
    Sube un archivo a un bucket de Google Cloud Storage.
    Retorna el URI del archivo en GCS (ej. gs://bucket/nombre_archivo).
    """
    print(f"2. Subiendo archivo a Google Cloud Storage: {file_path}")
    try:
        storage_client = storage.Client(project=GCP_PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob_name = os.path.basename(file_path)
        blob = bucket.blob(blob_name)

        blob.upload_from_filename(file_path)
        
        gcs_uri = f"gs://{bucket_name}/{blob_name}"
        print(f"   -> Archivo subido a: {gcs_uri}")
        return gcs_uri
    except Exception as e:
        print(f"   -> Error al subir a GCS: {e}")
        return None

def transcribir_audio_largo(gcs_uri):
    """
    Realiza la transcripción de un audio largo usando la API de Speech-to-Text.
    Retorna el texto transcrito.
    """
    print(f"3. Iniciando transcripción para: {gcs_uri}")
    start_time = time.time()
    
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    
    # Configuración del reconocimiento
    # Habilitamos la puntuación automática para un texto más legible
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100, # Tasa de muestreo estándar para MP3 de moviepy
        language_code=AUDIO_LANGUAGE_CODE,
        enable_automatic_punctuation=True,
    )

    try:
        # Inicia la operación de larga duración
        operation = client.long_running_recognize(config=config, audio=audio)
        print("   -> Esperando a que la transcripción finalice... (esto puede tardar varios minutos)")
        
        # Espera a que el trabajo termine
        response = operation.result(timeout=900) # Timeout de 15 minutos

        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript + "\n"
        
        end_time = time.time()
        print(f"   -> Transcripción completada en {int(end_time - start_time)} segundos.")
        return transcription

    except Exception as e:
        print(f"   -> Error durante la transcripción: {e}")
        return None

def guardar_transcripcion(video_path, texto):
    """
    Guarda el texto de la transcripción en un archivo .txt en la carpeta outputs.
    """
    base_name = os.path.basename(video_path)
    txt_filename = os.path.splitext(base_name)[0] + ".txt"
    txt_path = os.path.join("outputs", txt_filename)
    print(f"4. Guardando transcripción en: {txt_path}")
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(texto)
        print("   -> ¡Archivo de texto guardado!")
    except Exception as e:
        print(f"   -> Error al guardar el archivo: {e}")


def main(video_file_path):
    """
    Función principal que orquesta todo el proceso.
    """
    # Asegurarse de que el directorio de salida exista
    os.makedirs("outputs", exist_ok=True)

    if not os.path.exists(video_file_path):
        print(f"Error: El archivo de video no se encuentra en la ruta: {video_file_path}")
        return

    # 1. Extraer audio del video
    audio_file = extraer_audio(video_file_path)
    if not audio_file:
        return

    # 2. Subir audio a Google Cloud Storage
    gcs_uri = subir_a_gcs(audio_file, GCS_BUCKET_NAME)
    if not gcs_uri:
        return

    # 3. Transcribir el audio desde GCS
    texto_transcrito = transcribir_audio_largo(gcs_uri)
    if not texto_transcrito:
        return

    # 4. Guardar transcripción en archivo de texto
    guardar_transcripcion(video_file_path, texto_transcrito)
    
    # Opcional: Limpiar los archivos de audio locales
    os.remove(audio_file)
    print(f"\nProceso completado. Se eliminó el archivo de audio local: {os.path.basename(audio_file)}")


# --- CÓMO USAR EL SCRIPT ---
if __name__ == "__main__":
    # El script ahora acepta la ruta del video como un argumento de línea de comandos.
    # Ejemplo de uso:
    # python transcripcion.py "ruta/a/tu/video.mp4"

    if len(sys.argv) < 2:
        print("Uso: python transcripcion.py <ruta_del_video>")
        sys.exit(1)
        
    ruta_del_video = sys.argv[1]
    main(ruta_del_video)