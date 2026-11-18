#!/usr/bin/env python3
"""Descarga el audio de una entrevista de YouTube y la transcribe en local con Whisper (faster-whisper, GPU NVIDIA o CPU).

Uso:  .venv/Scripts/python herramientas/transcribir.py <slug> <url-de-youtube> "<Nombre del invitado>" ["glosario extra"]
Crea entrevistas/<slug>/ con: entrevista.m4a (no se sube al repo), info.txt, capitulos.json,
segmentos.json (texto con tiempos), transcripcion.txt (párrafos de ~1 min con marca [h:mm:ss]) y meta.json.

Es la versión para Windows/Linux del script original (que usaba MLX, solo para Mac con Apple Silicon).
El formato de salida es idéntico.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELO = "large-v3-turbo"
VENV = Path(sys.executable).parent


def hms(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def yt_dlp(*args):
    exe = VENV / ("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
    return [str(exe), "--js-runtimes", "node", *args]


def preparar_cuda():
    """Pone en el PATH las DLL de cuBLAS/cuDNN instaladas con pip (nvidia-cublas-cu12, nvidia-cudnn-cu12)."""
    base = Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    if not base.exists():
        return
    for b in base.glob("*/bin"):
        os.environ["PATH"] = str(b) + os.pathsep + os.environ["PATH"]
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(b))


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    slug, url, invitado = sys.argv[1:4]
    glosario = sys.argv[4] if len(sys.argv) > 4 else ""
    carpeta = RAIZ / "entrevistas" / slug
    carpeta.mkdir(parents=True, exist_ok=True)

    info = json.loads(subprocess.run(yt_dlp("--skip-download", "--dump-single-json", url),
                                     capture_output=True, text=True, encoding="utf-8", check=True).stdout)
    (carpeta / "capitulos.json").write_text(json.dumps(info.get("chapters") or [], ensure_ascii=False, indent=1), encoding="utf-8")
    (carpeta / "info.txt").write_text(f'{info["title"]} | {info.get("upload_date")} | {info.get("duration_string")} | '
                                      f'{info["webpage_url"]}\n{info.get("description", "")}\n', encoding="utf-8")
    audio = carpeta / "entrevista.m4a"
    if not audio.exists():
        subprocess.run(yt_dlp("-q", "-f", "bestaudio[ext=m4a]/bestaudio", "-o", str(audio), url), check=True)

    preparar_cuda()
    from faster_whisper import WhisperModel
    try:
        modelo = WhisperModel(MODELO, device="cuda", compute_type="float16")
    except Exception as e:  # sin GPU o sin las DLL de CUDA
        print("Sin GPU, uso CPU:", e)
        modelo = WhisperModel(MODELO, device="cpu", compute_type="int8")
    gen, _ = modelo.transcribe(
        str(audio), language="es", condition_on_previous_text=False,
        initial_prompt=(f"Entrevista de Ángel Gaitán a {invitado}. PSOE, PP, Vox, Sumar, Podemos, "
                        f"Junts, ERC, Bildu, PNV, Pedro Sánchez, Feijóo, Abascal, Moncloa, Congreso. {glosario}"))
    segs = []
    for s in gen:
        segs.append({"start": s.start, "end": s.end, "text": s.text})
        if len(segs) % 50 == 0:
            print(f"  {hms(s.end)}", flush=True)
    (carpeta / "segmentos.json").write_text(
        json.dumps([{"i": s["start"], "f": s["end"], "t": s["text"]} for s in segs], ensure_ascii=False), encoding="utf-8")
    with open(carpeta / "transcripcion.txt", "w", encoding="utf-8") as f:
        parrafo, ini = [], None
        for s in segs:
            if ini is None:
                ini = s["start"]
            parrafo.append(s["text"].strip())
            if s["end"] - ini >= 60:
                f.write(f"[{hms(ini)}] " + " ".join(parrafo) + "\n\n")
                parrafo, ini = [], None
        if parrafo:
            f.write(f"[{hms(ini)}] " + " ".join(parrafo) + "\n")

    d = int(info.get("duration") or 0)
    f = str(info.get("upload_date") or "")
    meses = "ene feb mar abr may jun jul ago sep oct nov dic".split()
    meta = {"slug": slug, "invitado": invitado, "programa": info["title"].split(" - ")[0], "video": info["id"],
            "fecha": f"{int(f[6:8])} {meses[int(f[4:6]) - 1]} {f[:4]}" if len(f) == 8 else "",
            "duracion": f"{d // 3600} h {d % 3600 // 60} min"}
    if not (carpeta / "meta.json").exists():
        (carpeta / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Hecho: {carpeta} · {len(segs)} segmentos · {len(info.get('chapters') or [])} capítulos")


if __name__ == "__main__":
    main()
