import subprocess

def run_enhancer(input_file_path, output_file_path):
    transcript = subprocess.check_output(
        [r"deepspeech", "--model", "deepspeech-0.9.3-models.pbmm", "--scorer", "deepspeech-0.9.3-models.scorer", "--audio", input_file_path]
    )
    with open(output_file_path, "w") as f:
        f.write(transcript.decode())
