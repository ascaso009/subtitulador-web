#!/usr/bin/env python3
import argparse
import os
from faster_whisper import WhisperModel
import argostranslate.package
import argostranslate.translate

def cmd_transcribe(args):
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(args.input, language=args.language, vad_filter=True)

    with open(args.output, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start = segment.start
            end = segment.end
            text = segment.text.strip()
            f.write(f"{i}\n{_format_time(start)} --> {_format_time(end)}\n{text}\n\n")

def _format_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
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
