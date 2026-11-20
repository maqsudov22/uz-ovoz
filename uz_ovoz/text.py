"""Matnni ovozlashtirishdan oldin tayyorlash."""

import re

# Kirill -> Lotin (o'zbek alifbosi). Ko'p harfli moslar avval tekshiriladi.
_CYR_TO_LAT = {
    "ё": "yo", "ю": "yu", "я": "ya", "ш": "sh", "ч": "ch", "ц": "ts",
    "ў": "oʻ", "ғ": "gʻ", "қ": "q", "ҳ": "h", "ъ": "ʼ", "ь": "",
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ж": "j",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "x", "ы": "i", "э": "e", "щ": "sh",
}

# o' / g' uchun ishlatiladigan turli apostroflar -> to'g'ri belgi (ʻ)
_OKINA_RE = re.compile(r"([oOgG])['`‘’ʼ´]")
# tutuq belgisi (ma'no, sur'at) -> ʼ
_TUTUQ_RE = re.compile(r"(?<=\w)['`‘’´](?=\w)")
_SPACES_RE = re.compile(r"[ \t]+")

_CYR_RE = re.compile(r"[Ѐ-ӿ]")


def has_cyrillic(text: str) -> bool:
    return bool(_CYR_RE.search(text))


def cyrillic_to_latin(text: str) -> str:
    out = []
    for i, ch in enumerate(text):
        low = ch.lower()
        # "е" so'z boshida va unlidan keyin "ye" bo'ladi
        if low == "е":
            prev = text[i - 1].lower() if i > 0 else " "
            lat = "ye" if (not prev.isalpha() or prev in "аеёиоуўэюяъь") else "e"
        else:
            lat = _CYR_TO_LAT.get(low)
        if lat is None:
            out.append(ch)
            continue
        if ch.isupper() and lat:
            nxt = text[i + 1] if i + 1 < len(text) else ""
            lat = lat.upper() if nxt.isupper() else lat[0].upper() + lat[1:]
        out.append(lat)
    return "".join(out)


def normalize(text: str) -> str:
    """Matnni TTS uchun tozalaydi: kirillni lotinga o'giradi, apostroflarni tuzatadi."""
    text = text.replace("\r\n", "\n").strip()
    if has_cyrillic(text):
        text = cyrillic_to_latin(text)
    text = _OKINA_RE.sub(lambda m: m.group(1) + "ʻ", text)
    text = _TUTUQ_RE.sub("ʼ", text)
    text = _SPACES_RE.sub(" ", text)
    return text
