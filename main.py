import math
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


def split_audio(input_file, output_folder, duration):
    print("start segment")
    audio = AudioSegment.from_mp3(input_file, parameters=['-nostdin'])
    total_length = len(audio)
    num_parts = math.ceil(total_length / (duration * 1000))
    print(num_parts)

    for i in range(num_parts):
        start = i * duration * 1000
        end = (i + 1) * duration * 1000
        split_audio = audio[start:end]
        output_path = os.path.join(output_folder, f"part_{i+1}.mp3")
        split_audio.export(output_path, format="mp3")
        print(f"Exported {output_path}")


def sort_key(filename):
    # Extract the numeric part from the filename using splitting and indexing
    return int(filename.split('_')[1].split('.')[0])


def transcriber(folder_name):
    filenames = []
    client = OpenAI(api_key=os.getenv("API_KEY"))
    print(f"Processing folder: {folder_name}")

    # Initialize an empty string to store combined transcript
    combined_transcript = ""

    # Get the full path of the folder
    full_folder_path = os.path.abspath(folder_name)
    # print(full_folder_path)
    for audio_filename in os.listdir(full_folder_path):
        filenames.append(audio_filename)

    # Sort the filenames using the custom sorting key
    sorted_filenames = sorted(filenames, key=sort_key)
    # Loop through each file in the specified folder
    for audio_filename in sorted_filenames:
        if audio_filename.endswith(".mp3"):
            # Construct the full path for the audio file
            full_audio_path = os.path.join(full_folder_path, audio_filename)
            print(f"Transcribing file: {full_audio_path}")

            with open(full_audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language="en"
                )
                individual_transcript = transcript
                print(f"Transcription for {audio_filename} completed.")

                # Save individual transcript to a separate file
                individual_filename = os.path.splitext(audio_filename)[
                    0] + ".txt"
                individual_file_path = os.path.join(
                    full_folder_path, individual_filename)
                with open(individual_file_path, "w") as individual_file:
                    individual_file.write(individual_transcript)
                    print(
                        f"Individual transcript saved: {individual_filename}")

                # Append transcript to the combined transcript
                combined_transcript += individual_transcript + "\n\n"

    # Write the combined transcript to a file
    combined_filename = f"{folder_name}_combined.txt"
    combined_file_path = os.path.join(full_folder_path, combined_filename)
    with open(combined_file_path, "w") as combined_file:
        combined_file.write(combined_transcript)
        print(f"Combined transcript saved: {combined_filename}")


def transcribe(event, context):
    input_file = "./voice_files/ustad_haniff_lecture_1.mp3"
    output_folder = "./output"
    duration = 300
    # after s3 trigger,this function will look through the s3 bucket path to process the voice file
    # within output folder must group according user emails/account
    # after processing,the combined.txt file must be saved in s3 bucket.
    print("start split audio")
    split_audio(input_file, output_folder, duration)
    print("start transcibe")
    transcriber(output_folder)
    print("Successful Execution")

# transcribe()
