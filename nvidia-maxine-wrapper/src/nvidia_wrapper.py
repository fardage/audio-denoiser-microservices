import textwrap
import subprocess
import os
from scipy.io.wavfile import read as read_wav


def write_config(input_file_path, output_file_path, args):
    config_file_path = output_file_path + ".cfg.txt"

    effect = "dereverb_denoiser"
    print(args.get("effect"))
    if args.get("effect") is not None:
        effect = args.get("effect")

    intensity_ratio = "1.0"
    if args.get("intensity_ratio") is not None:
        intensity_ratio = args.get("intensity_ratio")

    sample_rate, data = read_wav(input_file_path)
    model_sr = "16k"
    if sample_rate == 48000:
        model_sr = "48k"

    config = textwrap.dedent(
        f"""\
        effect {effect}
        sample_rate {sample_rate}
        model  /usr/local/AudioFX/models/sm_75/{effect}_{model_sr}.trtpkg
        real_time 0
        intensity_ratio {intensity_ratio}
        input_wav_list  {input_file_path}
        output_wav_list {output_file_path}
        """
    )

    with open(config_file_path, "w") as text_file:
        print(config, file=text_file)

    return config_file_path


def run_enhancer(config_filepath):
    subprocess.run(
        [r"/usr/local/AudioFX/samples/effects_demo/effects_demo", "-c", config_filepath]
    )


def cleanup(input_file_path, output_file_path, config_filepath):
    os.remove(input_file_path)
    os.remove(output_file_path)
    os.remove(config_filepath)
