#!/usr/bin/env python3
import argparse
import os
from faster_whisper import WhisperModel
import argostranslate.package
import argostranslate.translate

def cmd_transcribe(args):
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        args.input,
        language=args.language,
        vad_filter=True,
        word_timestamps=True
    )

    # Generar SRT normal
    with open(args.output, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = segment.start
            end = segment.end
            text = segment.text.strip()
            f.write(f"{i}\n{_format_time(start)} --> {_format_time(end)}\n{text}\n\n")

    # Generar ASS karaoke si se solicita
    if args.karaoke:
        karaoke_path = args.output.replace(".srt", "_karaoke.ass")
        _generar_ass_karaoke(segments, karaoke_path)

def _generar_ass_karaoke(segments, output_path):
    header = """[Script Info]
Title: Subtitulador Fácil - Modo Karaoke
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,50,1
Style: KaraokeHighlight,Arial,24,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2,1,2,10,10,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header)
        for segment in segments:
            if segment.words:
                start = _format_time_ass(segment.words[0].start)
                end = _format_time_ass(segment.words[-1].end)
                karaoke_line = ""
                for word in segment.words:
                    duration_cs = int((word.end - word.start) * 100)
                    karaoke_line += f"{{\\k{duration_cs}}}{word.word} "
                f.write(f"Dialogue: 0,{start},{end},KaraokeHighlight,,0,0,0,,{karaoke_line.strip()}\n")

def _format_time_ass(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def _format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    sec = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

def cmd_translate(args):
    from_lang = args.from_lang
    to_lang = args.to_lang

    installed = argostranslate.translate.get_installed_languages()
    has_from = any(l.code == from_lang for l in installed)
    has_to = any(l.code == to_lang for l in installed)
    if not (has_from and has_to):
        argostranslate.package.update_package_index()
        available = argostranslate.package.get_available_packages()
        for pkg in available:
            if pkg.from_code == from_lang and pkg.to_code == to_lang:
                argostranslate.package.install_from_path(pkg.download())
                break

    with open(args.input, encoding="utf-8") as f:
        content = f.read()

    blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
    translated_blocks = []
    for block in blocks:
        lines = block.split("\n")
        idx = lines[0]
        timestamp = lines[1]
        text = "\n".join(lines[2:])
        translated = argostranslate.translate.translate(text, from_lang, to_lang)
        translated_blocks.append(f"{idx}\n{timestamp}\n{translated}")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write("\n\n".join(translated_blocks) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p_trans = sub.add_parser("transcribe")
    p_trans.add_argument("input")
    p_trans.add_argument("-o", "--output", default="output.srt")
    p_trans.add_argument("--model", default="base", choices=["tiny","base","small","medium"])
    p_trans.add_argument("--language", default=None)
    p_trans.add_argument("--karaoke", action="store_true", help="Generar archivo ASS con modo karaoke")

    p_trad = sub.add_parser("translate")
    p_trad.add_argument("input")
    p_trad.add_argument("from_lang")
    p_trad.add_argument("to_lang")
    p_trad.add_argument("-o", "--output", default="translated.srt")

    args = parser.parse_args()
    if args.command == "transcribe":
        cmd_transcribe(args)
    elif args.command == "translate":
        cmd_translate(args)
