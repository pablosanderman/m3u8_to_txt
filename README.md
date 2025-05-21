# M3U8 to Text Converter

Converts m3u8 streams to MP3 and transcribes them using OpenAI's Whisper API.

## Requirements
- Python 3.8+
- ffmpeg
- OpenAI API key

## Usage
```
export OPENAI_API_KEY="your_openai_api_key"
```
```
python3 m3u8_to_txt.py
```

## Why this script?

I wanted to transcribe a lecture of a course I'm taking so that I can prompt ChatGPT to create anki flashcards for me. The website of the course uses m3u8 to stream the audio, so I wrote this script to convert the m3u8 to mp3 and then transcribe it using OpenAI's Whisper API.