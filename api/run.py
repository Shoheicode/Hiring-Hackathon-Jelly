from pydub.utils import mediainfo
import subprocess
import os
import json
import cv2
import string
import spacy

import whisper_timestamped as whisper


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


def transcribe_audiofile(audio_file: str):
    audio = whisper.load_audio(audio_file)
    model = whisper.load_model("base")

    result = whisper.transcribe(model, audio, language="en")

    arr = []
    for segment in result["segments"]:
        for word in segment["words"]:
            arr.append(
                {
                    "word": word["text"],
                    "start_seconds": word["start"],
                    "end_seconds": word["end"],
                }
            )

    return {"results": arr, "transcript": result["text"]}


def create_audio_transcript(file_path):
    channels, bit_rate, sample_rate = video_info(file_path)
    audio_path = video_to_audio(file_path, "audio.wav", channels, bit_rate, sample_rate)
    results = transcribe_audiofile(audio_path)

    with open("result.json", "w") as edited_file:
        json.dump(results, edited_file)


def add_captions_to_video(video_path, captions_json_path, output_path, keywords):
    # Read the video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read the captions JSON file
    with open(captions_json_path, "r") as f:
        captions = json.load(f)["results"]

    # Prepare the output video
    temp_output_path = "temp_output_without_audio.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    frame_number = 0
    caption_text = captions[0]["word"]
    next_word = captions[1]  # unsafe bc captions could be more
    word_index = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_number / fps

        # If the current_time is after the next_word's timestamp,
        # write that word to the captions
        if current_time >= next_word["start_seconds"]:
            caption_text = next_word["word"]

            word_index += 1
            if word_index < len(captions):
                next_word = captions[word_index]

        stripped_text = caption_text.translate(
            str.maketrans("", "", string.punctuation)
        )

        if stripped_text in keywords["named_entities"]:
            text_color = (255, 255, 0)
        elif stripped_text in keywords["nouns"]:
            text_color = (0, 0, 255)
        else:
            text_color = (255, 255, 255)

        textsize = cv2.getTextSize(caption_text, cv2.FONT_HERSHEY_TRIPLEX, 2, 2)[0]

        # get coords based on boundary
        textX = (width - textsize[0]) // 2
        textY = (height + textsize[1]) // 2

        cv2.putText(
            frame,
            caption_text,
            (textX, textY),
            cv2.FONT_HERSHEY_TRIPLEX,
            2,
            (0, 0, 0),
            8,
            cv2.LINE_AA,
        )

        cv2.putText(
            frame,
            caption_text,
            (textX, textY),
            cv2.FONT_HERSHEY_TRIPLEX,
            2,
            text_color,
            2,
            cv2.LINE_AA,
        )

        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()

    # Combine the captioned video with the original audio using FFmpeg
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        temp_output_path,
        "-i",
        video_path,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        output_path,
    ]

    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Video processing completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while processing the video: {e}")
    finally:
        # Remove the temporary file
        os.remove(temp_output_path)


# pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
def extract_keywords(file_path):
    nlp = spacy.load("en_core_web_sm")
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        text = data["transcript"]

        doc = nlp(text)
        # print(doc.ents)
        # for token in doc:
        #     print(
        #         token.text,
        #         # token.lemma_,
        #         "\t",
        #         token.pos_,
        #         "\t",
        #         token.tag_,
        #         "\t",
        #         token.dep_,
        #         # token.shape_,
        #         # token.is_alpha,
        #         # token.is_stop,
        #     )

        # mark ents and nouns as highlights
        return {
            "named_entities": set([str(ent) for ent in doc.ents]),
            "nouns": set([token.text for token in doc if token.pos_ == "NOUN"]),
        }


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    video_path = dir_path + r"\files\unedited.mp4"
    create_audio_transcript(video_path)

    # add captions to video
    captions_json_path = dir_path + r"\result.json"

    keywords = extract_keywords(captions_json_path)
    print(keywords)

    output_path = "output_video.mp4"
    add_captions_to_video(video_path, captions_json_path, output_path, keywords)
