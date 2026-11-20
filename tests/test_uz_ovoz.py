import asyncio

import pytest
from fastapi.testclient import TestClient

from uz_ovoz import tts
from uz_ovoz.app import app
from uz_ovoz.text import cyrillic_to_latin, normalize


class FakeCommunicate:
    calls = []

    def __init__(self, text, voice, **kw):
        FakeCommunicate.calls.append((text, voice, kw))

    async def stream(self):
        yield {"type": "WordBoundary"}
        yield {"type": "audio", "data": b"ID3fake"}
        yield {"type": "audio", "data": b"mp3"}


@pytest.fixture(autouse=True)
def fake_edge(monkeypatch):
    FakeCommunicate.calls.clear()
    monkeypatch.setattr(tts.edge_tts, "Communicate", FakeCommunicate)


def test_cyrillic_to_latin():
    assert cyrillic_to_latin("Салом дунё") == "Salom dunyo"
    assert cyrillic_to_latin("Ўзбекистон") == "Oʻzbekiston"
    assert cyrillic_to_latin("ғалаба") == "gʻalaba"
    assert cyrillic_to_latin("Ер ва келди") == "Yer va keldi"
    assert cyrillic_to_latin("ШАҲАР") == "SHAHAR"


def test_normalize_apostrophes():
    assert normalize("o'zbek g‘alaba") == "oʻzbek gʻalaba"
    assert normalize("ma'no") == "maʼno"
    assert normalize("  ko'p   bo'sh  joy ") == "koʻp boʻsh joy"


def test_synthesize_collects_audio():
    audio = asyncio.run(tts.synthesize("Salom", "sardor", rate=10, pitch=-5))
    assert audio == b"ID3fakemp3"
    text, voice, kw = FakeCommunicate.calls[0]
    assert voice == "uz-UZ-SardorNeural"
    assert kw == {"rate": "+10%", "pitch": "-5Hz", "volume": "+0%"}


@pytest.mark.parametrize("kwargs", [{"text": "   "}, {"text": "x", "voice": "nope"}, {"text": "x", "rate": 500}])
def test_synthesize_errors(kwargs):
    with pytest.raises(tts.TTSError):
        asyncio.run(tts.synthesize(**kwargs))


def test_api():
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert {v["key"] for v in client.get("/api/voices").json()} == {"madina", "sardor"}

    r = client.post("/api/tts", json={"text": "Салом"})
    assert r.status_code == 200
    assert r.headers["content-type"] == "audio/mpeg"
    assert FakeCommunicate.calls[-1][0] == "Salom"

    assert client.post("/api/tts", json={"text": "x", "voice": "nope"}).status_code == 400
    assert client.post("/api/tts", json={"text": "x", "rate": 999}).status_code == 422
