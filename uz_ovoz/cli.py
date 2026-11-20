"""Buyruq qatori: python -m uz_ovoz "Salom dunyo" -o salom.mp3"""

import argparse
import asyncio
import sys
from pathlib import Path

from . import tts


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="uz-ovoz", description="O'zbekcha matnni ovozga aylantirish")
    p.add_argument("text", nargs="?", help="Matn (berilmasa -f yoki stdin dan o'qiladi)")
    p.add_argument("-f", "--file", type=Path, help="Matnli fayl")
    p.add_argument("-o", "--output", type=Path, default=Path("ovoz.mp3"), help="Natija fayl (MP3)")
    p.add_argument("-v", "--voice", choices=list(tts.VOICES), default=tts.DEFAULT_VOICE)
    p.add_argument("-r", "--rate", type=int, default=0, help="Tezlik, foizda (-50..100)")
    p.add_argument("-p", "--pitch", type=int, default=0, help="Ohang, Hz da (-50..50)")
    args = p.parse_args(argv)

    if args.file:
        text = args.file.read_text(encoding="utf-8")
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        p.error("Matn kiriting")

    try:
        audio = asyncio.run(tts.synthesize(text, args.voice, args.rate, args.pitch))
    except tts.TTSError as exc:
        print(f"Xato: {exc}", file=sys.stderr)
        return 1
    args.output.write_bytes(audio)
    print(f"Saqlandi: {args.output} ({len(audio) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
