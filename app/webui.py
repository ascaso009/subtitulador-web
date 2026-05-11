import streamlit as st
import subprocess
import os
import re
import tempfile
import time
import argostranslate.package
import argostranslate.translate

st.set_page_config(page_title="Subtitulador Fácil", layout="centered")
st.title("🎬 Subtitulador Fácil")
st.markdown("Sube tu vídeo, genera subtítulos, tradúcelos y grábalos. **Todo automático.**")

# ---------- Estado persistente ----------
if "lang_pairs" not in st.session_state:
    st.session_state.lang_pairs = set()
if "ruta_srt_actual" not in st.session_state:
    st.session_state.ruta_srt_actual = None
if "ruta_video_actual" not in st.session_state:
    st.session_state.ruta_video_actual = None

# ---------- Preferencias de estilo guardadas ----------
DEFAULT_STYLE = {
    "font_size": 24,
    "font_name": "Impact",
    "font_color": "#FFFFFF",
    "margin_v": 50,
    "outline": 2,
    "shadow": 1,
}
for key, val in DEFAULT_STYLE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------- Funciones auxiliares ----------
def instalar_idioma(from_code, to_code):
    par = f"{from_code}->{to_code}"
    if par in st.session_state.lang_pairs:
        return True
    try:
        argostranslate.package.update_package_index()
        disponibles = argostranslate.package.get_available_packages()
        for pkg in disponibles:
            if pkg.from_code == from_code and pkg.to_code == to_code:
                with st.spinner(f"📥 Descargando diccionario {from_code}→{to_code}..."):
                    ruta_descargada = pkg.download()
                    argostranslate.package.install_from_path(ruta_descargada)
                st.session_state.lang_pairs.add(par)
                return True
        st.error(f"No se encontró el par {from_code} → {to_code}.")
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def obtener_duracion(video_path):
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return float(res.stdout.strip())
    except:
        return None

def transcribir_con_progreso(media_file, srt_out, model, language):
    duracion = obtener_duracion(media_file)
    barra = st.progress(0)
    estado = st.empty()
    estado.text("⏳ Analizando audio...")

    lang_arg = ["--language", language] if language != "auto" else []
    cmd = ["python3", "app/subtools.py", "transcribe", media_file,
           "-o", srt_out, "--model", model] + lang_arg

    proceso = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if duracion:
        inicio = time.time()
        while proceso.poll() is None:
            elapsed = time.time() - inicio
            factor = 3 if model in ["tiny", "base"] else 6
            progreso = min(elapsed / (duracion * factor), 0.99)
            barra.progress(progreso)
            estado.text(f"⏳ Transcribiendo... {int(progreso*100)}%")
            time.sleep(1)
    else:
        while proceso.poll() is None:
            time.sleep(1)

    proceso.wait()
    barra.progress(1.0)
    estado.text("✅ Transcripción completada.")
    return proceso.returncode, proceso.stderr.read()

def quemar_subtitulos_con_progreso(video_in, srt_in, estilo, video_out):
    duracion = obtener_duracion(video_in)
    barra = st.progress(0)
    estado = st.empty()

    cmd = [
        "ffmpeg", "-y",
        "-i", video_in,
        "-vf", f"subtitles={srt_in}:force_style='{estilo}'",
        "-c:a", "copy",
        "-progress", "pipe:1",
        "-nostats",
        video_out
    ]

    proceso = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for linea in proceso.stderr:
        if "time=" in linea:
            match = re.search(r"time=(\d+:\d+:\d+\.\d+)", linea)
            if match:
                tiempo_str = match.group(1)
                h, m, s = tiempo_str.split(":")
                segundos = float(h) * 3600 + float(m) * 60 + float(s)
                if duracion and duracion > 0:
                    progreso = min(segundos / duracion, 1.0)
                    barra.progress(progreso)
                    estado.text(f"🎬 Quemando... {int(progreso*100)}%")

    proceso.wait()
    barra.progress(1.0)
    estado.text("✅ Vídeo listo.")
    return proceso.returncode

# =====================================================================
# INTERFAZ PRINCIPAL
# =====================================================================

st.subheader("📁 1. Selecciona tu vídeo")
origen_vid = st.radio("Fuente del vídeo", ["Subir archivo", "Ruta en /data", "Usar último vídeo"], horizontal=True)
ruta_video = None
if origen_vid == "Subir archivo":
    vid_up = st.file_uploader("Sube tu vídeo", type=["mp4","mkv","mov","mp3","wav"], key="main_vid")
    if vid_up:
        suf = os.path.splitext(vid_up.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suf) as tmp:
            tmp.write(vid_up.read())
            ruta_video = tmp.name
        st.session_state.ruta_video_actual = ruta_video
elif origen_vid == "Ruta en /data":
    ruta = st.text_input("Ruta en /data", placeholder="/data/mi_video.mp4", key="main_ruta")
    if ruta and os.path.exists(ruta):
        ruta_video = ruta
        st.session_state.ruta_video_actual = ruta_video
    elif ruta:
        st.error("⚠️ Archivo no encontrado.")
else:
    if st.session_state.ruta_video_actual and os.path.exists(st.session_state.ruta_video_actual):
        st.info(f"🎬 Último vídeo: {os.path.basename(st.session_state.ruta_video_actual)}")
        ruta_video = st.session_state.ruta_video_actual
    else:
        st.warning("No hay vídeo anterior. Sube uno o indica una ruta.")

st.subheader("📄 2. Subtítulos (SRT)")
origen_srt = st.radio("Fuente del SRT", ["Generar nuevo", "Usar último SRT", "Subir .srt"], horizontal=True)
ruta_srt = None
if origen_srt == "Generar nuevo" and ruta_video:
    st.info("✨ Se generarán subtítulos automáticamente del vídeo seleccionado.")
elif origen_srt == "Usar último SRT":
    if st.session_state.ruta_srt_actual and os.path.exists(st.session_state.ruta_srt_actual):
        st.info(f"📄 Último SRT: {os.path.basename(st.session_state.ruta_srt_actual)}")
        ruta_srt = st.session_state.ruta_srt_actual
    else:
        st.warning("No hay SRT anterior.")
elif origen_srt == "Subir .srt":
    srt_up = st.file_uploader("Sube tu .srt", type=["srt"], key="main_srt")
    if srt_up:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".srt", mode="w", encoding="utf-8") as tmp:
            tmp.write(srt_up.read().decode("utf-8"))
            ruta_srt = tmp.name
        st.session_state.ruta_srt_actual = ruta_srt

if origen_srt == "Generar nuevo" and ruta_video:
    st.subheader("⚙️ Opciones de transcripción")
    c1, c2, c3 = st.columns(3)
    with c1:
        idioma = st.selectbox("Idioma del audio", ["auto","es","en","fr","de","pt","it","nl","ru","zh","ja","ar"])
    with c2:
        precision = st.selectbox("Precisión", ["tiny","base","small","medium"], index=1)
    with c3:
        traducir_despues = st.checkbox("Traducir después", value=False)
        if traducir_despues:
            to_lang = st.selectbox("Traducir a", ["es","en","fr","de","pt","it","nl","ru","zh","ja","ar"], index=1)

st.subheader("🎨 Estilo de los subtítulos")
c_tam, c_fuente, c_color = st.columns(3)
with c_tam:
    st.session_state.font_size = st.slider("Tamaño", 12, 60, st.session_state.font_size)
with c_fuente:
    st.session_state.font_name = st.selectbox("Fuente", [
        "Impact", "Liberation Sans Bold", "Liberation Sans", "DejaVu Sans Bold", "DejaVu Sans"
    ], index=0)
with c_color:
    st.session_state.font_color = st.color_picker("Color", st.session_state.font_color)

c_pos, c_out, c_sha = st.columns(3)
with c_pos:
    st.session_state.margin_v = st.slider("Posición vertical", 10, 200, st.session_state.margin_v, step=10)
with c_out:
    st.session_state.outline = st.slider("Contorno", 0, 5, st.session_state.outline)
with c_sha:
    st.session_state.shadow = st.slider("Sombra", 0, 5, st.session_state.shadow)

st.markdown("---")
if st.button("🚀 ¡PROCESAR TODO!", type="primary", use_container_width=True, disabled=not ruta_video):
    if not ruta_video:
        st.error("Selecciona un vídeo primero.")
    else:
        if origen_srt == "Generar nuevo":
            srt_out = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name
            returncode, stderr = transcribir_con_progreso(ruta_video, srt_out, precision, idioma)
            if returncode != 0:
                st.error(f"❌ Error al transcribir: {stderr}")
                st.stop()
            os.chmod(srt_out, 0o644)
            ruta_srt = srt_out
            st.session_state.ruta_srt_actual = srt_out
            st.success("✅ Subtítulos generados.")

        if traducir_despues and ruta_srt:
            if not instalar_idioma(idioma if idioma != "auto" else "es", to_lang):
                st.stop()
            srt_trad = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name
            cmd = ["python3", "app/subtools.py", "translate", ruta_srt, idioma if idioma != "auto" else "es", to_lang, "-o", srt_trad]
            with st.spinner("🌍 Traduciendo..."):
                res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                st.error(f"❌ Error al traducir: {res.stderr}")
            else:
                os.chmod(srt_trad, 0o644)
                ruta_srt = srt_trad
                st.session_state.ruta_srt_actual = srt_trad
                st.success(f"✅ Traducido a {to_lang}.")

        if ruta_srt:
            hex_color = st.session_state.font_color.lstrip('#')
            r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
            ass_color = f"&H{b}{g}{r}&"
            estilo = f"FontSize={st.session_state.font_size},FontName={st.session_state.font_name},PrimaryColour={ass_color}"
            estilo += f",MarginV={st.session_state.margin_v}"
            if st.session_state.outline > 0:
                estilo += f",Outline={st.session_state.outline}"
            if st.session_state.shadow > 0:
                estilo += f",Shadow={st.session_state.shadow}"

            video_out = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
            returncode = quemar_subtitulos_con_progreso(ruta_video, ruta_srt, estilo, video_out)

            if returncode != 0:
                st.error("❌ Error al quemar subtítulos.")
            else:
                os.chmod(video_out, 0o644)
                with open(video_out, "rb") as f:
                    video_bytes = f.read()

                st.success("🎉 ¡VÍDEO LISTO!")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.video(video_bytes)
                    st.caption("⬆️ Previsualización. Descarga el vídeo con el botón de abajo.")
                st.download_button("📥 Descargar vídeo con subtítulos", video_bytes,
                                   file_name="video_con_subtitulos.mp4", mime="video/mp4")
        else:
            st.error("No se pudo obtener un SRT para quemar.")
