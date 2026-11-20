"""Veb-ilova: brauzerda matn yozib, ovozini eshitish."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

from . import tts

STATIC = Path(__file__).parent / "static"

app = FastAPI(title="uz-ovoz", description="O'zbekcha matnni ovozga aylantirish")


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=tts.MAX_CHARS * 2)
    voice: str = tts.DEFAULT_VOICE
    rate: int = Field(0, ge=-50, le=100)
    pitch: int = Field(0, ge=-50, le=50)
    volume: int = Field(0, ge=-50, le=100)


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/voices")
def voices():
    return [{"key": k, **v} for k, v in tts.VOICES.items()]


@app.post("/api/tts")
async def text_to_speech(req: TTSRequest):
    try:
        audio = await tts.synthesize(req.text, req.voice, req.rate, req.pitch, req.volume)
    except tts.TTSError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="uz-ovoz.mp3"'},
    )


def main():
    import os

    import uvicorn

    uvicorn.run(app, host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "8000")))


if __name__ == "__main__":
    main()
