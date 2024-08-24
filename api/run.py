# Imports the Google Cloud client library


from google.cloud import speech
from pydub.utils import mediainfo
import subprocess
import os


def video_info(video_filepath):
    """this function returns number of channels, bit rate, and sample rate of the video"""

    video_data = mediainfo(video_filepath)
    print(video_data)
    channels = video_data["channels"]
    bit_rate = video_data["bit_rate"]
    sample_rate = video_data["sample_rate"]

    return channels, bit_rate, sample_rate


def video_to_audio(
    video_filepath, audio_filename, video_channels, video_bit_rate, video_sample_rate
):
    command = f"ffmpeg -i {video_filepath} -b:a {video_bit_rate} -ac {video_channels} -ar {video_sample_rate} -vn {audio_filename}"
    subprocess.call(command, shell=True)
    blob_name = f"audios/{audio_filename}"
    return blob_name


def run_quickstart() -> speech.RecognizeResponse:
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")


if __name__ == "__main__":
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # print(dir_path)

    file_path = r"C:\Users\ianbb\Documents\Code\headstarter\Hiring-Hackathon-Jelly\api\files\edited.mp4"
    channels, bit_rate, sample_rate = video_info(file_path)
    audio_path = video_to_audio(file_path, "audio.wav", channels, bit_rate, sample_rate)
    print(audio_path)
