"""
Loudness Report, v2. 2022-09-05
"""
import soundfile as sf
import pyloudnorm as pyln
import os
from pydub import AudioSegment
import datetime
import pprint


def list_wav_files(path):  # List all wav-files in working_path.
    wav_files = []
    print("\nFound the following wav-files:\n")

    for file in os.listdir(path):
        if file == ".DS_Store":
            continue
        name, ext = os.path.splitext(file)
        # print(f"name: {name} + ext{ext}")
        if ext == ".wav":
            print(f"filename: {file}")
            wav_files.append(file)
    wav_files.sort()
    print(f"wav_files: {wav_files}")
    return wav_files


def lufs_measuring(file, working_path):
    audiofile = os.path.join(working_path, file)
    data, rate = sf.read(audiofile)  # Load audio (with shape (samples, channels))
    meter = pyln.Meter(rate)  # create BS.1770 meter
    loudness = meter.integrated_loudness(data)  # measure loudness
    print(file, "LUFS:", round(loudness, 2))
    return loudness


def report_writer(tiedostonimi, list_of_dicts, start):  # TODO: List of dictionaries for inputting data to this
    """
        pituus = len(file)

        spacing = "\t"  # + "\t" + "\t"
        longspacing = " " * (50 - pituus)
        namelength = 0
        nlname = "N/A
        if len(file) > namelength:
            namelength = len(file)
            nlname = file
        print("The longest filename was: " + nlname + " at " + str(namelength) + " characters.")
    """

    longspacing = "       "
    spacing = " | "
    # print(type(list_of_dicts))
    # print(list_of_dicts)
    with open(tiedostonimi, "w") as tiedosto:
        tiedosto.write(
            "LUFS report generated by loudness-test.py version 2.0 / Programmed by Daniel Hjerppe" + "\n" +
            "Using libraries: soundfile, pyloudnorm and pydub" + "\n" + "\n")

        for data in list_of_dicts:
            print(data["name"])
            tiedosto.write(data["name"] + longspacing +
                           "LUFS: " + str(round(data["loudness"], 2)) + spacing +
                           "Max Peak: " + str(round(data["maxPeak"], 2)) + spacing +
                           "Samplerate: " + str(data["framesPerSecond"]) + spacing +
                           "Bitrate: " + str(data["bytesPerSample"]) + "\n")

        tiedosto.write("\n" + "\n" + "This report was automatically generated on: " + str(datetime.datetime.now()))
        tiedosto.write("\n" + "Time taken to generate: " + str(datetime.datetime.now() - start) + "\n")


def main(start):  # Main orchestrator. Takes input begintime to calculate time for report.
    current_path = os.path.dirname(os.path.realpath(__file__))
    # working_path = os.path.join(base_path, "Google Drive", "Kuusikoski E-Studio")
    working_path = current_path
    tiedostonimi = os.path.join(working_path, "LUFS.txt")
    list_of_dicts = []

    print("current_path =", current_path)
    print("Selected working_path is =", working_path)

    wav_files = list_wav_files(working_path)  # Finds all wav files in "working_path". Outputs a list of files.

    for file in wav_files:  # Measures wav file LUFS and other attributes, outputs to a list of dictionaries.
        loudness = lufs_measuring(file, working_path)
        sound = AudioSegment.from_file(os.path.join(working_path, file))
        max_peak = sound.max_dBFS
        frames_per_second = sound.frame_rate
        bytes_per_sample = sound.sample_width
        try:
            bytes_per_sample = bytes_per_sample * 8
        except ValueError:
            bytes_per_sample = "N/A"

        wav_dict = {
            "name": file,
            "loudness": loudness,
            "maxPeak": max_peak,
            "framesPerSecond": frames_per_second,
            "bytesPerSample": bytes_per_sample,
        }
        list_of_dicts.append(wav_dict)

    print(f"\nItems on list_of_dicts: {len(list_of_dicts)}\n")
    pprint.pprint(list_of_dicts)

    report_writer(tiedostonimi, list_of_dicts, start)  # Writes the report. Inputs: filename, audiodata(dict) and start


if __name__ == "__main__":
    begintime = datetime.datetime.now()
    main(begintime)
