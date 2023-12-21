import speech_recognition as sr
from pydub import AudioSegment
import os

def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def transcribe_audio(wav_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source) 
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
    return text

def generate_subtitles(text, chunk_length=10):
    words = text.split()
    chunks = []
    chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1 
        if current_length > chunk_length:
            chunks.append(" ".join(chunk))
            chunk = [word]
            current_length = len(word) + 1
        else:
            chunk.append(word)

    if chunk:
        chunks.append(" ".join(chunk))

    return chunks

def create_srt_file(subtitles, output_path):
    with open(output_path, 'w') as file:
        for idx, subtitle in enumerate(subtitles):
            start_time = idx * 10  
            end_time = (idx + 1) * 10
            start_time_str = format_time(start_time)
            end_time_str = format_time(end_time)
            file.write(f"{idx + 1}\n")
            file.write(f"{start_time_str} --> {end_time_str}\n")
            file.write(f"{subtitle}\n\n")

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    milliseconds = 0  
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def mp3_to_subtitles(mp3_path, srt_output_path):
    if not os.path.exists(mp3_path):
        print(f"Error: The file {mp3_path} does not exist!")
        return

    wav_path = mp3_path.replace(".mp3", ".wav")
    mp3_to_wav(mp3_path, wav_path)

    text = transcribe_audio(wav_path)
    if not text:
        print("Error: No text transcribed. Check the audio quality or try again.")
        return

    subtitles = generate_subtitles(text)

    create_srt_file(subtitles, srt_output_path)

    os.remove(wav_path)

    print(f"Subtitles saved to {srt_output_path}")

mp3_path = 'motivationalspeech.mp3' 
srt_output_path = 'output_subtitles.srt'
mp3_to_subtitles(mp3_path, srt_output_path)
