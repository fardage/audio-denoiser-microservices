import subprocess

def run_enhancer():
    subprocess.run(
        ["./run.sh", "VER=resnet-1.1n", "INFER=1", "GAIN=\'deepmmse\'"]
    )
