import streamlit as st
import subprocess
import os
import re
import tempfile
import time
import argostranslate.package
import argostranslate.translate

# =====================================================================
# TRADUCCIONES (ES, EN, GL, FR)
# =====================================================================
T = {
    "es": {
        "title": "🎬 Subtitulador Fácil",
        "subtitle": "Sube tu vídeo, genera subtítulos, tradúcelos y grábalos. **Todo automático.**",
        "help_title": "ℹ️ ¿Cómo uso esta herramienta?",
        "help_text": """
        1. **Elige una tarea** en el menú de abajo.
        2. **Sube un archivo** o indica la ruta dentro de la carpeta `/data`.
        3. Configura las opciones y pulsa el botón para procesar.
        4. **Descarga el resultado** cuando aparezca el mensaje de éxito.
        """,
        "step1": "📁 1. Selecciona tu vídeo",
        "vid_source": "Fuente del vídeo",
        "vid_upload": "Subir archivo",
        "vid_path": "Ruta en /data",
        "vid_last": "Usar último vídeo",
        "vid_upload_btn": "Sube tu vídeo",
        "vid_path_placeholder": "/data/mi_video.mp4",
        "vid_last_info": "🎬 Último vídeo: ",
        "vid_not_found": "⚠️ Archivo no encontrado.",
        "vid_no_last": "No hay vídeo anterior. Sube uno o indica una ruta.",
        "step2": "📄 2. Subtítulos (SRT)",
        "srt_source": "Fuente del SRT",
        "srt_generate": "Generar nuevo",
        "srt_last": "Usar último SRT",
        "srt_upload": "Subir .srt",
        "srt_generate_info": "✨ Se generarán subtítulos automáticamente del vídeo seleccionado.",
        "srt_last_info": "📄 Último SRT: ",
        "srt_no_last": "No hay SRT anterior.",
        "srt_upload_btn": "Sube tu .srt",
        "transcribe_options": "⚙️ Opciones de transcripción",
        "lang_audio": "Idioma del audio",
        "precision": "Precisión",
        "translate_after": "Traducir después",
        "translate_to": "Traducir a",
        "style": "🎨 Estilo de los subtítulos",
        "size": "Tamaño",
        "font": "Fuente",
        "color": "Color",
        "position": "Posición vertical",
        "outline": "Contorno",
        "shadow": "Sombra",
        "process_btn": "🚀 ¡PROCESAR TODO!",
        "select_vid_first": "Selecciona un vídeo primero.",
        "transcribing": "⏳ Analizando audio...",
        "transcribing_progress": "⏳ Transcribiendo... ",
        "transcription_done": "✅ Transcripción completada.",
        "srt_generated": "✅ Subtítulos generados.",
        "translating": "🌍 Traduciendo...",
        "translated": "✅ Traducido a ",
        "burning": "🎬 Quemando... esto puede tardar según la duración del vídeo.",
        "video_ready": "🎉 ¡VÍDEO LISTO!",
        "preview_caption": "⬆️ Previsualización. Descarga el vídeo con el botón de abajo.",
        "download_btn": "📥 Descargar vídeo con subtítulos",
        "video_done": "✅ Vídeo listo.",
        "no_srt": "No se pudo obtener un SRT para quemar.",
        "error_transcribe": "❌ Error al transcribir: ",
        "error_translate": "❌ Error al traducir: ",
        "error_burn": "❌ Error al quemar subtítulos.",
        "error_lang_pair": "No se encontró el par {} → {}.",
        "error_generic": "Error: ",
        "downloading_dict": "📥 Descargando diccionario {}→{} (solo la primera vez)...",
        "video_lost": "❌ El vídeo original no está disponible.",
        "video_empty": "❌ El vídeo resultante está vacío o corrupto.",
        "ffmpeg_error": "Error ejecutando ffmpeg: ",
        "ffmpeg_timeout": "❌ El proceso tardó demasiado (más de 1 hora).",
        "burn_success": "✅ Vídeo quemado correctamente.",
    },
    "en": {
        "title": "🎬 Easy Subtitler",
        "subtitle": "Upload your video, generate subtitles, translate them and burn them in. **Fully automatic.**",
        "help_title": "ℹ️ How to use this tool?",
        "help_text": """
        1. **Choose a task** from the menu below.
        2. **Upload a file** or enter the path inside the `/data` folder.
        3. Configure the options and click the button to process.
        4. **Download the result** when the success message appears.
        """,
        "step1": "📁 1. Select your video",
        "vid_source": "Video source",
        "vid_upload": "Upload file",
        "vid_path": "Path in /data",
        "vid_last": "Use last video",
        "vid_upload_btn": "Upload your video",
        "vid_path_placeholder": "/data/my_video.mp4",
        "vid_last_info": "🎬 Last video: ",
        "vid_not_found": "⚠️ File not found.",
        "vid_no_last": "No previous video. Upload one or enter a path.",
        "step2": "📄 2. Subtitles (SRT)",
        "srt_source": "SRT source",
        "srt_generate": "Generate new",
        "srt_last": "Use last SRT",
        "srt_upload": "Upload .srt",
        "srt_generate_info": "✨ Subtitles will be automatically generated from the selected video.",
        "srt_last_info": "📄 Last SRT: ",
        "srt_no_last": "No previous SRT.",
        "srt_upload_btn": "Upload your .srt",
        "transcribe_options": "⚙️ Transcription options",
        "lang_audio": "Audio language",
        "precision": "Precision",
        "translate_after": "Translate afterwards",
        "translate_to": "Translate to",
        "style": "🎨 Subtitle style",
        "size": "Size",
        "font": "Font",
        "color": "Color",
        "position": "Vertical position",
        "outline": "Outline",
        "shadow": "Shadow",
        "process_btn": "🚀 PROCESS ALL!",
        "select_vid_first": "Select a video first.",
        "transcribing": "⏳ Analyzing audio...",
        "transcribing_progress": "⏳ Transcribing... ",
        "transcription_done": "✅ Transcription completed.",
        "srt_generated": "✅ Subtitles generated.",
        "translating": "🌍 Translating...",
        "translated": "✅ Translated to ",
        "burning": "🎬 Burning... this may take a while depending on video length.",
        "video_ready": "🎉 VIDEO READY!",
        "preview_caption": "⬆️ Preview. Download the video with the button below.",
        "download_btn": "📥 Download video with subtitles",
        "video_done": "✅ Video ready.",
        "no_srt": "Could not obtain an SRT to burn.",
        "error_transcribe": "❌ Error transcribing: ",
        "error_translate": "❌ Error translating: ",
        "error_burn": "❌ Error burning subtitles.",
        "error_lang_pair": "Language pair {} → {} not found.",
        "error_generic": "Error: ",
        "downloading_dict": "📥 Downloading dictionary {}→{} (first time only)...",
        "video_lost": "❌ The original video is not available.",
        "video_empty": "❌ The resulting video is empty or corrupt.",
        "ffmpeg_error": "Error running ffmpeg: ",
        "ffmpeg_timeout": "❌ The process took too long (more than 1 hour).",
        "burn_success": "✅ Video burned successfully.",
    },
    "gl": {
        "title": "🎬 Subtitulador Fácil",
        "subtitle": "Sube o teu vídeo, xera subtítulos, tradúceos e grávaos. **Todo automático.**",
        "help_title": "ℹ️ Como usar esta ferramenta?",
        "help_text": """
        1. **Elixe unha tarefa** no menú de abaixo.
        2. **Sube un ficheiro** ou indica a ruta dentro do cartafol `/data`.
        3. Configura as opcións e preme o botón para procesar.
        4. **Descarga o resultado** cando apareza a mensaxe de éxito.
        """,
        "step1": "📁 1. Selecciona o teu vídeo",
        "vid_source": "Orixe do vídeo",
        "vid_upload": "Subir ficheiro",
        "vid_path": "Ruta en /data",
        "vid_last": "Usar último vídeo",
        "vid_upload_btn": "Sube o teu vídeo",
        "vid_path_placeholder": "/data/meu_video.mp4",
        "vid_last_info": "🎬 Último vídeo: ",
        "vid_not_found": "⚠️ Ficheiro non atopado.",
        "vid_no_last": "Non hai vídeo anterior. Sube un ou indica unha ruta.",
        "step2": "📄 2. Subtítulos (SRT)",
        "srt_source": "Orixe do SRT",
        "srt_generate": "Xerar novo",
        "srt_last": "Usar último SRT",
        "srt_upload": "Subir .srt",
        "srt_generate_info": "✨ Xeraranse subtítulos automaticamente do vídeo seleccionado.",
        "srt_last_info": "📄 Último SRT: ",
        "srt_no_last": "Non hai SRT anterior.",
        "srt_upload_btn": "Sube o teu .srt",
        "transcribe_options": "⚙️ Opcións de transcrición",
        "lang_audio": "Idioma do audio",
        "precision": "Precisión",
        "translate_after": "Traducir despois",
        "translate_to": "Traducir a",
        "style": "🎨 Estilo dos subtítulos",
        "size": "Tamaño",
        "font": "Fonte",
        "color": "Cor",
        "position": "Posición vertical",
        "outline": "Contorno",
        "shadow": "Sombra",
        "process_btn": "🚀 PROCESAR TODO!",
        "select_vid_first": "Selecciona un vídeo primeiro.",
        "transcribing": "⏳ Analizando audio...",
        "transcribing_progress": "⏳ Transcribindo... ",
        "transcription_done": "✅ Transcrición completada.",
        "srt_generated": "✅ Subtítulos xerados.",
        "translating": "🌍 Traducindo...",
        "translated": "✅ Traducido a ",
        "burning": "🎬 Gravando... isto pode tardar segundo a duración do vídeo.",
        "video_ready": "🎉 VÍDEO LISTO!",
        "preview_caption": "⬆️ Previsualización. Descarga o vídeo co botón de abaixo.",
        "download_btn": "📥 Descargar vídeo con subtítulos",
        "video_done": "✅ Vídeo listo.",
        "no_srt": "Non se puido obter un SRT para gravar.",
        "error_transcribe": "❌ Erro ao transcribir: ",
        "error_translate": "❌ Erro ao traducir: ",
        "error_burn": "❌ Erro ao gravar subtítulos.",
        "error_lang_pair": "Non se atopou o par {} → {}.",
        "error_generic": "Erro: ",
        "downloading_dict": "📥 Descargando dicionario {}→{} (só a primeira vez)...",
        "video_lost": "❌ O vídeo orixinal non está dispoñible.",
        "video_empty": "❌ O vídeo resultante está baleiro ou corrupto.",
        "ffmpeg_error": "Erro executando ffmpeg: ",
        "ffmpeg_timeout": "❌ O proceso tardou demasiado (máis de 1 hora).",
        "burn_success": "✅ Vídeo gravado correctamente.",
    },
    "fr": {
        "title": "🎬 Sous-titreur Facile",
        "subtitle": "Téléchargez votre vidéo, générez des sous-titres, traduisez-les et incrustez-les. **Entièrement automatique.**",
        "help_title": "ℹ️ Comment utiliser cet outil ?",
        "help_text": """
        1. **Choisissez une tâche** dans le menu ci-dessous.
        2. **Téléchargez un fichier** ou indiquez le chemin dans le dossier `/data`.
        3. Configurez les options et cliquez sur le bouton pour traiter.
        4. **Téléchargez le résultat** lorsque le message de succès apparaît.
        """,
        "step1": "📁 1. Sélectionnez votre vidéo",
        "vid_source": "Source de la vidéo",
        "vid_upload": "Télécharger un fichier",
        "vid_path": "Chemin dans /data",
        "vid_last": "Utiliser la dernière vidéo",
        "vid_upload_btn": "Téléchargez votre vidéo",
        "vid_path_placeholder": "/data/ma_video.mp4",
        "vid_last_info": "🎬 Dernière vidéo : ",
        "vid_not_found": "⚠️ Fichier introuvable.",
        "vid_no_last": "Aucune vidéo précédente. Téléchargez-en une ou indiquez un chemin.",
        "step2": "📄 2. Sous-titres (SRT)",
        "srt_source": "Source du SRT",
        "srt_generate": "Générer un nouveau",
        "srt_last": "Utiliser le dernier SRT",
        "srt_upload": "Télécharger .srt",
        "srt_generate_info": "✨ Les sous-titres seront générés automatiquement à partir de la vidéo sélectionnée.",
        "srt_last_info": "📄 Dernier SRT : ",
        "srt_no_last": "Aucun SRT précédent.",
        "srt_upload_btn": "Téléchargez votre .srt",
        "transcribe_options": "⚙️ Options de transcription",
        "lang_audio": "Langue de l'audio",
        "precision": "Précision",
        "translate_after": "Traduire ensuite",
        "translate_to": "Traduire en",
        "style": "🎨 Style des sous-titres",
        "size": "Taille",
        "font": "Police",
        "color": "Couleur",
        "position": "Position verticale",
        "outline": "Contour",
        "shadow": "Ombre",
        "process_btn": "🚀 TOUT TRAITER !",
        "select_vid_first": "Sélectionnez d'abord une vidéo.",
        "transcribing": "⏳ Analyse de l'audio...",
        "transcribing_progress": "⏳ Transcription... ",
        "transcription_done": "✅ Transcription terminée.",
        "srt_generated": "✅ Sous-titres générés.",
        "translating": "🌍 Traduction...",
        "translated": "✅ Traduit en ",
        "burning": "🎬 Incrustation... cela peut prendre du temps selon la durée de la vidéo.",
        "video_ready": "🎉 VIDÉO PRÊTE !",
        "preview_caption": "⬆️ Aperçu. Téléchargez la vidéo avec le bouton ci-dessous.",
        "download_btn": "📥 Télécharger la vidéo avec sous-titres",
        "video_done": "✅ Vidéo prête.",
        "no_srt": "Impossible d'obtenir un SRT à incruster.",
        "error_transcribe": "❌ Erreur de transcription : ",
        "error_translate": "❌ Erreur de traduction : ",
        "error_burn": "❌ Erreur d'incrustation des sous-titres.",
        "error_lang_pair": "Paire de langues {} → {} introuvable.",
        "error_generic": "Erreur : ",
        "downloading_dict": "📥 Téléchargement du dictionnaire {}→{} (première fois seulement)...",
        "video_lost": "❌ La vidéo originale n'est pas disponible.",
        "video_empty": "❌ La vidéo résultante est vide ou corrompue.",
        "ffmpeg_error": "Erreur lors de l'exécution de ffmpeg : ",
        "ffmpeg_timeout": "❌ Le processus a pris trop de temps (plus d'une heure).",
        "burn_success": "✅ Vidéo incrustée avec succès.",
    },
}

# =====================================================================
# CONFIGURACIÓN INICIAL
# =====================================================================
st.set_page_config(page_title="Subtitulador Fácil", layout="centered")

if "lang" not in st.session_state:
    st.session_state.lang = "es"

# Selector de idioma
col_lang1, col_lang2 = st.columns([5, 1])
with col_lang2:
    idiomas_ui = {"🇪🇸 Español": "es", "🇬🇧 English": "en", "🇬🇱 Galego": "gl", "🇫🇷 Français": "fr"}
    seleccion = st.selectbox("idioma", list(idiomas_ui.keys()),
                             index=list(idiomas_ui.values()).index(st.session_state.lang),
                             label_visibility="collapsed")
    st.session_state.lang = idiomas_ui[seleccion]

L = T[st.session_state.lang]

st.title(L["title"])
st.markdown(L["subtitle"])

with st.expander(L["help_title"], expanded=False):
    st.markdown(L["help_text"])

# ---------- Estado persistente ----------
if "lang_pairs" not in st.session_state:
    st.session_state.lang_pairs = set()
if "ruta_srt_actual" not in st.session_state:
    st.session_state.ruta_srt_actual = None
if "ruta_video_actual" not in st.session_state:
    st.session_state.ruta_video_actual = None

DEFAULT_STYLE = {
    "font_size": 24,
    "font_name": "Liberation Sans Bold",
    "font_color": "#FFFFFF",
    "margin_v": 50,
    "outline": 2,
    "shadow": 1,
}
for key, val in DEFAULT_STYLE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------- Mapeo de códigos de idioma a nombres ----------
LANG_CODES = {
    "Auto": "auto",
    "Español": "es", "English": "en", "Français": "fr", "Deutsch": "de",
    "Português": "pt", "Italiano": "it", "Nederlands": "nl",
    "Русский": "ru", "中文": "zh", "日本語": "ja", "العربية": "ar"
}

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
                with st.spinner(L["downloading_dict"].format(from_code, to_code)):
                    ruta_descargada = pkg.download()
                    argostranslate.package.install_from_path(ruta_descargada)
                st.session_state.lang_pairs.add(par)
                return True
        st.error(L["error_lang_pair"].format(from_code, to_code))
        return False
    except Exception as e:
        st.error(f"{L['error_generic']}{e}")
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
    estado.text(L["transcribing"])

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
            estado.text(f"{L['transcribing_progress']}{int(progreso*100)}%")
            time.sleep(1)
    else:
        while proceso.poll() is None:
            time.sleep(1)

    proceso.wait()
    barra.progress(1.0)
    estado.text(L["transcription_done"])
    return proceso.returncode, proceso.stderr.read()

def quemar_subtitulos_simple(video_in, srt_in, estilo, video_out):
    """Quema subtítulos SIN barra de progreso, mucho más fiable."""
    estado = st.empty()
    estado.text(L["burning"])

    cmd = [
        "ffmpeg", "-y",
        "-i", video_in,
        "-vf", f"subtitles={srt_in}:force_style='{estilo}'",
        "-c:a", "copy",
        video_out
    ]

    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if resultado.returncode != 0:
            st.error(f"{L['error_burn']}\n{resultado.stderr[-500:]}")
            estado.text("")
            return resultado.returncode
        estado.text(L["burn_success"])
        return 0
    except subprocess.TimeoutExpired:
        st.error(L["ffmpeg_timeout"])
        return -1
    except Exception as e:
        st.error(f"{L['ffmpeg_error']}{e}")
        return -1

# =====================================================================
# INTERFAZ PRINCIPAL
# =====================================================================

st.subheader(L["step1"])
origen_vid = st.radio(L["vid_source"], [L["vid_upload"], L["vid_path"], L["vid_last"]], horizontal=True)
ruta_video = None
if origen_vid == L["vid_upload"]:
    vid_up = st.file_uploader(L["vid_upload_btn"], type=["mp4","mkv","mov","mp3","wav"], key="main_vid")
    if vid_up:
        suf = os.path.splitext(vid_up.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suf) as tmp:
            tmp.write(vid_up.read())
            ruta_video = tmp.name
        st.session_state.ruta_video_actual = ruta_video
elif origen_vid == L["vid_path"]:
    ruta = st.text_input(L["vid_path"], placeholder=L["vid_path_placeholder"], key="main_ruta")
    if ruta and os.path.exists(ruta):
        ruta_video = ruta
        st.session_state.ruta_video_actual = ruta_video
    elif ruta:
        st.error(L["vid_not_found"])
else:
    if st.session_state.ruta_video_actual and os.path.exists(st.session_state.ruta_video_actual):
        st.info(f"{L['vid_last_info']}{os.path.basename(st.session_state.ruta_video_actual)}")
        ruta_video = st.session_state.ruta_video_actual
    else:
        st.warning(L["vid_no_last"])

st.subheader(L["step2"])
origen_srt = st.radio(L["srt_source"], [L["srt_generate"], L["srt_last"], L["srt_upload"]], horizontal=True)
ruta_srt = None
if origen_srt == L["srt_generate"] and ruta_video:
    st.info(L["srt_generate_info"])
elif origen_srt == L["srt_last"]:
    if st.session_state.ruta_srt_actual and os.path.exists(st.session_state.ruta_srt_actual):
        st.info(f"{L['srt_last_info']}{os.path.basename(st.session_state.ruta_srt_actual)}")
        ruta_srt = st.session_state.ruta_srt_actual
    else:
        st.warning(L["srt_no_last"])
elif origen_srt == L["srt_upload"]:
    srt_up = st.file_uploader(L["srt_upload_btn"], type=["srt"], key="main_srt")
    if srt_up:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".srt", mode="w", encoding="utf-8") as tmp:
            tmp.write(srt_up.read().decode("utf-8"))
            ruta_srt = tmp.name
        st.session_state.ruta_srt_actual = ruta_srt

if origen_srt == L["srt_generate"] and ruta_video:
    st.subheader(L["transcribe_options"])
    c1, c2, c3 = st.columns(3)
    with c1:
        nombres_idiomas = list(LANG_CODES.keys())
        idioma_nombre = st.selectbox(L["lang_audio"], nombres_idiomas, index=0)
        idioma = LANG_CODES[idioma_nombre]
    with c2:
        precision = st.selectbox(L["precision"], ["tiny","base","small","medium"], index=1)
    with c3:
        traducir_despues = st.checkbox(L["translate_after"], value=False)
        if traducir_despues:
            nombres_destino = [n for n in nombres_idiomas if n != "Auto"]
            to_lang_nombre = st.selectbox(L["translate_to"], nombres_destino, index=1)
            to_lang = LANG_CODES[to_lang_nombre]

st.subheader(L["style"])
c_tam, c_fuente, c_color = st.columns(3)
with c_tam:
    st.session_state.font_size = st.slider(L["size"], 12, 60, st.session_state.font_size)
with c_fuente:
    st.session_state.font_name = st.selectbox(L["font"], [
        "Liberation Sans Bold", "Liberation Sans", "DejaVu Sans Bold", "DejaVu Sans", "DejaVu Sans Mono"
    ], index=0)
with c_color:
    st.session_state.font_color = st.color_picker(L["color"], st.session_state.font_color)

c_pos, c_out, c_sha = st.columns(3)
with c_pos:
    st.session_state.margin_v = st.slider(L["position"], 10, 200, st.session_state.margin_v, step=10)
with c_out:
    st.session_state.outline = st.slider(L["outline"], 0, 5, st.session_state.outline)
with c_sha:
    st.session_state.shadow = st.slider(L["shadow"], 0, 5, st.session_state.shadow)

st.markdown("---")
if st.button(L["process_btn"], type="primary", use_container_width=True, disabled=not ruta_video):
    if not ruta_video:
        st.error(L["select_vid_first"])
    else:
        # Inicializar variables por si no se definieron
        if 'traducir_despues' not in dir() and 'traducir_despues' not in locals():
            traducir_despues = False
        if 'to_lang' not in dir() and 'to_lang' not in locals():
            to_lang = "en"
        if 'to_lang_nombre' not in dir() and 'to_lang_nombre' not in locals():
            to_lang_nombre = "English"

        if origen_srt == L["srt_generate"]:
            srt_out = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name
            returncode, stderr = transcribir_con_progreso(ruta_video, srt_out, precision, idioma)
            if returncode != 0:
                st.error(f"{L['error_transcribe']}{stderr}")
                st.stop()
            os.chmod(srt_out, 0o644)
            ruta_srt = srt_out
            st.session_state.ruta_srt_actual = srt_out
            st.success(L["srt_generated"])

        if traducir_despues and ruta_srt:
            if not instalar_idioma(idioma if idioma != "auto" else "es", to_lang):
                st.stop()
            srt_trad = tempfile.NamedTemporaryFile(delete=False, suffix=".srt").name
            cmd = ["python3", "app/subtools.py", "translate", ruta_srt, idioma if idioma != "auto" else "es", to_lang, "-o", srt_trad]
            with st.spinner(L["translating"]):
                res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                st.error(f"{L['error_translate']}{res.stderr}")
            else:
                os.chmod(srt_trad, 0o644)
                ruta_srt = srt_trad
                st.session_state.ruta_srt_actual = srt_trad
                st.success(f"{L['translated']}{to_lang_nombre}")

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
            if not ruta_video or not os.path.exists(ruta_video):
                st.error(L["video_lost"])
            else:
                returncode = quemar_subtitulos_simple(ruta_video, ruta_srt, estilo, video_out)
                if returncode != 0:
                    st.error(L["error_burn"])
                else:
                    os.chmod(video_out, 0o644)
                    with open(video_out, "rb") as f:
                        video_bytes = f.read()
                    if len(video_bytes) < 1000:
                        st.error(L["video_empty"])
                    else:
                        st.success(L["video_ready"])
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.video(video_bytes)
                            st.caption(L["preview_caption"])
                        st.download_button(L["download_btn"], video_bytes,
                                           file_name="video_con_subtitulos.mp4", mime="video/mp4")
        else:
            st.error(L["no_srt"])
