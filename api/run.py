# Imports the Google Cloud client library


from google.cloud import speech
from pydub.utils import mediainfo
import subprocess
import os
import json
import cv2
import numpy as np
import time

import threading
from playsound import playsound

dir_path = os.path.dirname(os.path.realpath(__file__))
credentials_path = dir_path + r"\credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path


def video_info(video_filepath):
    """this function returns number of channels, bit rate, and sample rate of the video"""

    video_data = mediainfo(video_filepath)

    channels = video_data["channels"]
    bit_rate = video_data["bit_rate"]
    sample_rate = video_data["sample_rate"]

    return channels, bit_rate, sample_rate


def video_to_audio(
    video_filepath, audio_filename, video_channels, video_bit_rate, video_sample_rate
):
    command = f"ffmpeg -i {video_filepath} -b:a {video_bit_rate} -ac 1 -ar {video_sample_rate} -vn {audio_filename}"
    subprocess.call(command, shell=True)
    # blob_name = f"audios/{audio_filename}"

    return audio_filename


def transcribe_audiofile(audio_file: str) -> speech.RecognizeResponse:
    # Instantiates a client
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)

    config = {
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "language_code": "en-US",
        "enable_word_time_offsets": True,
        "model": "video",
    }

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    arr = []
    for result in response.results:
        best_alt = result.alternatives[0]

        for word_info in best_alt.words:
            try:
                start_time = word_info.start_time
                end_time = word_info.end_time
            except:
                pass

            # print(word_info.word)
            # print(start_time.seconds)
            # print(start_time.microseconds)
            # print(end_time.seconds)
            # print(end_time.microseconds)
            print()

            arr.append(
                {
                    "word": word_info.word,
                    "start_seconds": start_time.seconds
                    + (start_time.microseconds / 1000000),
                    "end_seconds": end_time.seconds
                    + +(end_time.microseconds / 1000000),
                }
            )

        # print(f"Transcript: {result.alternatives[0].transcript}")
    return {"results": arr}


def create_audio_transcript(file_path):
    channels, bit_rate, sample_rate = video_info(file_path)
    audio_path = video_to_audio(file_path, "audio.wav", channels, bit_rate, sample_rate)
    results = transcribe_audiofile(audio_path)

    # adds more buffer between words if their start_seconds are the same
    results = results["results"]
    last_time = [results[0]["start_seconds"], 1]

    for i in range(1, len(results)):
        if results[i]["start_seconds"] == last_time[0]:
            if i + 1 < len(results):
                if (
                    results[i]["start_seconds"] + 0.4 * last_time[1]
                    >= results[i + 1]["start_seconds"]
                    and results[i + 1]["start_seconds"] != last_time[0]
                ):
                    results[i]["start_seconds"] += (
                        results[i + 1]["start_seconds"] - results[i]["start_seconds"]
                    ) / 2
                else:
                    results[i]["start_seconds"] += 0.4 * last_time[1]
                    last_time[1] += 1
        else:
            last_time = [results[i]["start_seconds"], 1]

    with open("result.json", "w") as edited_file:
        json.dump({"results": results}, edited_file)


def add_captions_to_video(video_path, captions_json_path, output_path):
    # Read the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read the captions JSON file
    with open(captions_json_path, "r") as f:
        captions = json.load(f)["results"]

    # Prepare the output video
    temp_output_path = 'temp_output_without_audio.mp4'
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    frame_number = 0
    caption_text = captions[0]["word"]
    next_word = captions[1] # unsafe bc captions could be more
    word_index = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_number / fps

        # Check if there's a caption for this time
        # caption_text = word_info["word"]
        if current_time >= next_word["start_seconds"]:
            caption_text = next_word["word"]

            word_index += 1
            if word_index < len(captions):
                next_word = captions[word_index]

        # if caption_text:
        #     # Add caption to the frame
        cv2.putText(
            frame,
            caption_text,
            (100, height // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()

    # Combine the captioned video with the original audio using FFmpeg
    ffmpeg_command = [
        'ffmpeg',
        '-i', temp_output_path,
        '-i', video_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        output_path
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Video processing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while processing the video: {e}")
    finally:
        # Remove the temporary file
        os.remove(temp_output_path)


def play_audio_and_write_captions_to_terminal():
    t = threading.Thread(
        target=lambda: playsound(
            r"C:\Users\ianbb\Documents\Code\headstarter\Hiring-Hackathon-Jelly\api\audio.wav"
        )
    )

    t.start()
    print("started")

    with open("result_edited.json", "r") as json_file:
        data = json.load(json_file)
        initial_time = time.time()

        for word_info in data["results"]:
            word = word_info["word"]
            start_seconds = word_info["start_seconds"]

            target_time = initial_time + start_seconds

            while time.time() < target_time:
                a = 0

            os.system("cls" if os.name == "nt" else "clear")
            print(word)

    t.join()


if __name__ == "__main__":
    running = False

    if running:
        play_audio_and_write_captions_to_terminal()
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = dir_path + r"\files\edited_better.mp4"
        # create_audio_transcript(file_path)

        # add captions to video
        video_path = dir_path + r"\files\edited_better.mp4"
        captions_json_path = dir_path + r"\result.json"
        output_path = "output_video.mp4"
        add_captions_to_video(video_path, captions_json_path, output_path)
