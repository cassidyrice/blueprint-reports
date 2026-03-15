
import os
import re
import time

# --- CONFIGURATION ---
DRAFTS_DIR = r"c:\Users\abvik\OneDrive\Desktop\Hotel\drafts"
OUTPUT_DIR = r"c:\Users\abvik\OneDrive\Desktop\Hotel\audiobook"

# Voice engine: "gtts" (free, no key) or "google_cloud" (high quality, needs credentials)
ENGINE = os.getenv("TTS_ENGINE", "google_cloud")

# Google Cloud settings (only used if ENGINE = "google_cloud")
# Get credentials at: https://console.cloud.google.com/apis/credentials
# Set this env var: GOOGLE_APPLICATION_CREDENTIALS=path\to\your-key.json
# Voice options:
#   Neural2 (best free tier): en-US-Neural2-D (male, deep, authoritative)
#   WaveNet (great free tier): en-US-Wavenet-D (male, calm, clear)
#   Studio (near-human, paid):  en-US-Studio-M (male, premium audiobook quality)
GC_VOICE_NAME   = "en-US-Neural2-D"      # Deep, authoritative male narrator
GC_VOICE_GENDER = "MALE"
GC_LANGUAGE     = "en-US"

# Order: Preface first, then chapters in order
CHAPTER_ORDER = (
    ["PREFACE.md"] +
    [f"CHAPTER_{str(i).zfill(2)}.md" for i in range(1, 26)]
)

# ---------------------------------------------------------------------------

def clean_markdown(text):
    text = re.sub(r'^#{1,4} .+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{1,2}', '', text)
    text = re.sub(r'In the next chapter,.*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def generate_gtts(text, out_path):
    from gtts import gTTS
    tts = gTTS(text=text, lang='en', tld='com', slow=False)
    tts.save(out_path)

def generate_google_cloud(text, out_path):
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient()

    # Split into chunks ≤ 5000 bytes (GC limit is 5000 chars per request)
    chunks = [text[i:i+4800] for i in range(0, len(text), 4800)]
    all_audio = b""

    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            print(f"      chunk {i+1}/{len(chunks)}...")
        synthesis_input = texttospeech.SynthesisInput(text=chunk)
        voice = texttospeech.VoiceSelectionParams(
            language_code=GC_LANGUAGE,
            name=GC_VOICE_NAME,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, GC_VOICE_GENDER)
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.95,   # Slightly slower for an audiobook feel
            pitch=-1.0            # Slightly deeper/more resonant tone
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        all_audio += response.audio_content

    with open(out_path, "wb") as f:
        f.write(all_audio)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    to_process = [f for f in CHAPTER_ORDER
                  if os.path.isfile(os.path.join(DRAFTS_DIR, f))]

    engine_label = "Google Cloud Neural2" if ENGINE == "google_cloud" else "Google TTS (free)"
    print(f"Analog Algorithm — Audiobook Generator ({engine_label})")
    print(f"Voice: {GC_VOICE_NAME if ENGINE == 'google_cloud' else 'gTTS en-US'}")
    print(f"Processing {len(to_process)} chapters → {OUTPUT_DIR}")
    print("-" * 60)

    for filename in to_process:
        src_path = os.path.join(DRAFTS_DIR, filename)
        out_name = filename.replace(".md", ".mp3")
        out_path = os.path.join(OUTPUT_DIR, out_name)

        if os.path.exists(out_path):
            print(f"  [SKIP]  {filename}")
            continue

        print(f"  [TTS]   {filename}...")
        with open(src_path, "r", encoding="utf-8") as f:
            clean = clean_markdown(f.read())

        if not clean:
            print(f"  [WARN]  Empty after cleaning. Skipping.")
            continue

        try:
            if ENGINE == "google_cloud":
                generate_google_cloud(clean, out_path)
            else:
                generate_gtts(clean, out_path)
            size_kb = os.path.getsize(out_path) // 1024
            print(f"  [DONE]  {out_name} ({size_kb} KB)")
        except Exception as e:
            print(f"  [ERR]   {filename}: {e}")

        time.sleep(0.5)

    print("-" * 60)
    print("Audiobook generation complete.")

if __name__ == "__main__":
    main()
