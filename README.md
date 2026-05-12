# 🎬 Subtitulador Fácil

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-ascaso99%2Fsubtitulador--web-blue?logo=docker)](https://hub.docker.com/r/ascaso99/subtitulador-web)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Idiomas](https://img.shields.io/badge/idiomas-español%20%7C%20english%20%7C%20galego-brightgreen)]()

Herramienta web para **transcribir, traducir e incrustar subtítulos** en vídeos.  
**100% offline** tras la primera descarga de modelos. **Sin terminal, sin complicaciones.**

<p align="center">
  <img src="https://img.shields.io/badge/Whisper-OpenAI-orange?logo=openai" alt="Whisper">
  <img src="https://img.shields.io/badge/Traducción-10%2B%20idiomas-blueviolet" alt="Idiomas">
  <img src="https://img.shields.io/badge/Fuente-Impact-red" alt="Impact">
</p>

---

## ✨ Funcionalidades

| 🎤 Transcripción | 🌐 Traducción | 🎞️ Quemado |
|---|---|---|
| IA Whisper de OpenAI | 10+ idiomas offline | Fuente Impact y más |
| Auto-detección de idioma | Diccionarios offline | Tamaño, color, posición |
| Modelos tiny a medium | Chino, ruso, japonés... | Contorno y sombra |

- 🧠 **Un solo botón** para transcribir → traducir → quemar
- 📥 **Previsualización** del vídeo antes de descargar
- 🎨 **Estilo personalizable** que se guarda para siempre
- 🌍 **Interfaz multilingüe**: 🇪🇸 Español | 🇬🇧 English | 🇬🇱 Galego
- 🐳 **Imagen Docker pública** lista para usar

---

## 🚀 Instalación rápida (2 comandos)

```bash
git clone https://github.com/ascaso009/subtitulador-web.git
cd subtitulador-web
docker compose up
  

Abre http://localhost:8501 y sigue los 3 pasos en pantalla.

O con Docker directamente

docker run -p 8501:8501 -v ./mis_videos:/data ascaso99/subtitulador-web:latest

📁 Montar tus archivos

Crea una carpeta mis_videos junto al proyecto y pon tus vídeos ahí.
Dentro del contenedor estarán en /data/.
También puedes subirlos directamente desde la interfaz web.

bash

mkdir mis_videos
cp /ruta/a/tu_video.mp4 mis_videos/

En la web, selecciona "Ruta en /data" y escribe /data/tu_video.mp4.
🛠 Requisitos

Docker y Docker Compose

Conexión a internet solo la primera vez (descarga modelos de IA)

Después: 100% offline, incluso la traducción

📸 Captura de pantalla



📦 Docker Hub

Imagen precompilada disponible en:
👉 ascaso99/subtitulador-web
bash

docker pull ascaso99/subtitulador-web:latest

🧑‍💻 Desarrollo
bash

git clone https://github.com/ascaso009/subtitulador-web.git
cd subtitulador-web
docker compose up --build

Los modelos de Whisper y traducción se descargan automáticamente la primera vez.
📝 Licencia

MIT - Libre para usar, modificar y compartir.

Hecho con ❤️ por @ascaso009
