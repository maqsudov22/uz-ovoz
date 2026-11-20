# uz-ovoz

Oʻzbekcha matnni ovozga (MP3) aylantiruvchi dastur. Ikki xil ovoz bor:

| Ovoz   | Turi  |
|--------|-------|
| Madina | ayol  |
| Sardor | erkak |

Ovozlar Microsoft Edge TTS xizmati orqali bepul yaratiladi (internet kerak, API kalit kerak emas).

**Imkoniyatlar**
- Lotin va kirill yozuvi (kirill avtomatik lotinga oʻgiriladi)
- `o'`, `g'` dagi turli apostroflarni toʻgʻrilaydi
- Tezlik va ohangni sozlash
- Veb-sahifa (tinglash + MP3 yuklab olish) va buyruq qatori (CLI)
- Bir martada 5000 belgigacha

## Oʻrnatish

Python 3.10+ kerak.

```bash
git clone https://github.com/maqsudov22/uz-ovoz.git
cd uz-ovoz
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Veb-sahifa

```bash
python -m uz_ovoz.app
```

Soʻng brauzerda oching: http://127.0.0.1:8000

## Buyruq qatori

```bash
python -m uz_ovoz "Assalomu alaykum, qalaysiz?" -o salom.mp3
python -m uz_ovoz "Салом дунё" -v sardor -r 20 -o salom.mp3
python -m uz_ovoz -f kitob.txt -o kitob.mp3
```

| Parametr | Maʼnosi |
|----------|---------|
| `-o` | natija fayl (standart: `ovoz.mp3`) |
| `-v` | ovoz: `madina` yoki `sardor` |
| `-r` | tezlik, foizda (-50..100) |
| `-p` | ohang, Hz da (-50..50) |
| `-f` | matnni fayldan oʻqish |

## API

`POST /api/tts` — javob `audio/mpeg`:

```json
{"text": "Salom", "voice": "madina", "rate": 0, "pitch": 0}
```

`GET /api/voices` — mavjud ovozlar roʻyxati.

## Testlar

```bash
pip install pytest httpx
python -m pytest
```
