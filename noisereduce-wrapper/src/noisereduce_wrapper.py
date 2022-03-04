from scipy.io import wavfile
import noisereduce as nr

def run_enhancer(input_file_path, output_file_path, args):
    stationary = False
    print(args.get("stationary"))
    if args.get("stationary") is not None:
        stationary = args.get("stationary") == 'True'

    rate, data = wavfile.read(input_file_path)
    reduced_noise = nr.reduce_noise(y=data, sr=rate, stationary=stationary)
    wavfile.write(output_file_path, rate, reduced_noise)