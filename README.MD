# 🎧 Transcripción de Videos con Google Cloud Speech-to-Text

Script en Python que:
1) extrae el **audio** de un video (MP4 → MP3),
2) sube el audio a **Google Cloud Storage (GCS)**,
3) ejecuta una **transcripción asíncrona** con **Speech-to-Text**,
4) guarda el resultado en un **.txt** junto al video original.

> Probado con `moviepy`, `google-cloud-speech` y `google-cloud-storage`.

---

## 🗂 Estructura sugerida del proyecto

app-transcripcion-videos/
├─ transcripcion.py
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ videos/ # (opcional) fuente de videos
├─ outputs/ # (opcional) a- .mp3 b- .txt
└─ secrets/ # claves/credenciales (NO se versionan)

markdown
Copiar
Editar

> Puedes mantener tus videos en `videos/` y las salidas en `outputs/`. Ajusta rutas según tu preferencia.

---

## ✅ Requisitos

- **Python 3.10.7**
- Cuenta de **Google Cloud** con:
  - Proyecto habilitado (`urbanvibe-pruebas` u otro)
  - API **Speech-to-Text** habilitada
  - **Bucket** GCS creado (por ej. `speech_to_text_esm_pruebas`)
  - **Credencial de servicio** (JSON)
- **FFmpeg** instalado (requerido por `moviepy` para manipular audio/video)

### Instalar FFmpeg
- Windows: `choco install ffmpeg` (o descarga desde la web oficial)
- macOS: `brew install ffmpeg`
- Linux (Debian/Ubuntu): `sudo apt-get install ffmpeg`

---

## 🔐 Autenticación GCP

Guarda tu **clave JSON** de cuenta de servicio en `./secrets/` y exporta la variable:

```bash
# Windows (PowerShell)
$env:GOOGLE_APPLICATION_CREDENTIALS = ".\secrets\mi-servicio.json"

# macOS / Linux
export GOOGLE_APPLICATION_CREDENTIALS="./secrets/mi-servicio.json"
🧩 Instalación
bash
Copiar
Editar
# 1) Crear y activar entorno virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Instalar dependencias
pip install -r requirements.txt
# Si no tienes requirements.txt todavía:
# pip install google-cloud-speech google-cloud-storage moviepy
requirements.txt (sugerido):

txt
Copiar
Editar
google-cloud-speech>=2.27.0
google-cloud-storage>=2.18.0
moviepy>=1.0.3
⚙️ Configuración del script
En transcripcion.py, verifica/ajusta:

python
Copiar
Editar
GCP_PROJECT_ID = "urbanvibe-pruebas"
GCS_BUCKET_NAME = "speech_to_text_esm_pruebas"
AUDIO_LANGUAGE_CODE = "es-CL"
Recomendación futura: leer estos valores desde variables de entorno para evitar hardcode (ej. os.getenv("GCS_BUCKET_NAME")).

▶️ Uso
Opción A: editar la ruta dentro del script
En la sección if __name__ == "__main__": cambia ruta_del_video por la ruta a tu archivo:

python
Copiar
Editar
ruta_del_video = "videos/mi_video.mp4"
y luego ejecuta:

bash
Copiar
Editar
python transcripcion.py
Opción B (mejora rápida): pasar la ruta por argumento
Ejemplo rápido (si agregas un sys.argv):

bash
Copiar
Editar
python transcripcion.py "videos/mi_video.mp4"
Si te interesa, te paso el snippet para aceptar argumentos inmediatamente.

📄 Salidas
mi_video.mp3 (audio extraído)

mi_video.txt (transcripción final)

