from pydub.utils import mediainfo
import whisper_timestamped as whisper

import spacy
import subprocess
import pathlib
import json

from caption_creator import add_captions_to_video


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


def create_audio_transcript(file_path, result_path):
    audio_file_path = "audio.wav"
    channels, bit_rate, sample_rate = video_info(file_path)
    video_to_audio(file_path, audio_file_path, channels, bit_rate, sample_rate)
    results = transcribe_audiofile(audio_file_path)

    with open(result_path, "w") as edited_file:
        json.dump(results, edited_file)


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
    video_path_str = r"files\edited_better.mp4"
    dir_path = pathlib.Path(__file__).parent
    video_path = dir_path.joinpath(video_path_str)

    json_path = r"result.json"
    captions_json_path = dir_path.joinpath(json_path)

    create_audio_transcript(video_path, captions_json_path)

    # add captions to video
    keywords = extract_keywords(captions_json_path)
    print(keywords)

    output_path = "output_video.mp4"
    add_captions_to_video(video_path, captions_json_path, output_path, keywords)
