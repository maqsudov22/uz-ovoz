"""Ovoz yaratish (Microsoft Edge TTS, o'zbek ovozlari)."""

import edge_tts

from .text import normalize

VOICES = {
    "madina": {"id": "uz-UZ-MadinaNeural", "name": "Madina", "gender": "ayol"},
    "sardor": {"id": "uz-UZ-SardorNeural", "name": "Sardor", "gender": "erkak"},
}
DEFAULT_VOICE = "madina"
MAX_CHARS = 5000


class TTSError(Exception):
    pass


def _percent(value: int) -> str:
    return f"{value:+d}%"


def _hz(value: int) -> str:
    return f"{value:+d}Hz"


async def synthesize(
    text: str,
    voice: str = DEFAULT_VOICE,
    rate: int = 0,
    pitch: int = 0,
    volume: int = 0,
) -> bytes:
    """Matndan MP3 audio yaratadi.

    rate/volume: -50..+100 foiz, pitch: -50..+50 Hz.
    """
    if voice not in VOICES:
        raise TTSError(f"Noma'lum ovoz: {voice}. Mavjudlari: {', '.join(VOICES)}")
    clean = normalize(text)
    if not clean:
        raise TTSError("Matn bo'sh")
    if len(clean) > MAX_CHARS:
        raise TTSError(f"Matn juda uzun (maksimal {MAX_CHARS} belgi)")
    if not -50 <= rate <= 100 or not -50 <= volume <= 100 or not -50 <= pitch <= 50:
        raise TTSError("Tezlik, balandlik yoki ovoz qiymati chegaradan tashqarida")

    communicate = edge_tts.Communicate(
        clean,
        VOICES[voice]["id"],
        rate=_percent(rate),
        pitch=_hz(pitch),
        volume=_percent(volume),
    )
    audio = bytearray()
    try:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.extend(chunk["data"])
    except Exception as exc:  # tarmoq xatolari va h.k.
        raise TTSError(f"Ovoz xizmatiga ulanib bo'lmadi: {exc}") from exc
    if not audio:
        raise TTSError("Ovoz yaratilmadi")
    return bytes(audio)
