import cv2
import string
import json
import subprocess
import pathlib


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
    next_word = captions[1] if 1 < len(captions) else None
    word_index = 1
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_number / fps

        # If the current_time is after the next_word's timestamp,
        # write that word to the captions
        if next_word:
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
        pathlib.Path(temp_output_path).unlink()
