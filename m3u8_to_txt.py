import os
import subprocess
from urllib.parse import urlparse
from openai import OpenAI
import time

# Get OpenAI API key from environment variable or prompt user
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = input("Enter your OpenAI API key: ")
    
# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def convert_m3u8_to_mp3(input_url, output_file):
    # Construct the ffmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
        "-i", input_url,
        "-vn",
        "-c:a", "libmp3lame", "-b:a", "128k",
        output_file
    ]

    print(f"Converting {input_url} to {output_file}...")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Conversion complete! File saved as: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return False

def transcribe_audio(audio_file_path):
    print(f"Transcribing {audio_file_path}...")
    
    try:
        with open(audio_file_path, "rb") as audio_file:
            # Call OpenAI Whisper API using the new client format
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
            return transcription.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def save_transcription(text, output_file):
    # Create the transcriptions directory if it doesn't exist
    transcriptions_dir = "transcriptions"
    os.makedirs(transcriptions_dir, exist_ok=True)
    
    # Get just the filename without path
    filename = os.path.basename(output_file)
    
    # Create the full path in the transcriptions directory
    output_path = os.path.join(transcriptions_dir, filename)
    
    with open(output_path, "w") as f:
        f.write(text)
    print(f"Transcription saved to {output_path}")

def main():
    input_url = input("Enter the m3u8 url: ")
    output_mp3 = input("Enter the output MP3 filename (or press Enter for auto-name): ")

    # Generate output filename if not provided
    if not output_mp3:
        # Extract filename from URL and replace extension
        parsed_url = urlparse(input_url)
        base_name = os.path.basename(parsed_url.path).split('.')[0]
        output_mp3 = f"{base_name}.mp3"
    
    # Generate transcript filename
    transcript_file = os.path.splitext(output_mp3)[0] + ".txt"
    
    # Step 1: Convert m3u8 to MP3
    conversion_success = convert_m3u8_to_mp3(input_url, output_mp3)
    
    if conversion_success:
        # Step 2: Transcribe MP3 to text
        transcription = transcribe_audio(output_mp3)
        
        if transcription:
            # Step 3: Save transcription to file
            save_transcription(transcription, transcript_file)
            
            # Step 4: Delete the MP3 file
            try:
                os.remove(output_mp3)
                print(f"MP3 file {output_mp3} has been deleted.")
            except Exception as e:
                print(f"Error deleting MP3 file: {e}")
                
            print("Process completed successfully!")
        else:
            print("Transcription failed.")
    else:
        print("MP3 conversion failed. Cannot proceed with transcription.")

if __name__ == "__main__":
    main()



