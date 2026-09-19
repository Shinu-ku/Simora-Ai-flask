from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import requests
from backend.config import settings

router = APIRouter()

class VoiceRequest(BaseModel):
    text: str

@router.post("/synthesize")
def synthesize_voice(request: VoiceRequest):
    if not settings.ELEVENLABS_API_KEY:
        # Fallback will be handled by frontend
        raise HTTPException(status_code=501, detail="ElevenLabs not configured")

    voice_id = settings.ELEVENLABS_VOICE_ID or "21m00Tcm4TlvDq8ikWAM" # default voice
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }
    
    data = {
        "text": request.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to synthesize audio")
            
        return Response(content=response.content, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
