import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from transcript import *
from melo.api import TTS
import traceback

parento = "./RealAudios"
speakeros = []
for folderName in os.listdir(parento):
    folderPath = os.path.join(parento, folderName)
    if os.path.isdir(folderPath) and folderName.startswith('speaker'):
        speakeros.append(folderName)

ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

source_se = torch.load(f'checkpoints_v2/base_speakers/ses/en-india.pth', map_location=device)   # using en-india as the speakers are from India
speaker_id=2    # speaker_id 2 is for the same reason
speed = 1.0
log_file_path = "logs.txt" # file to save logs
language = "EN"

for speaker in speakeros:
    input_dir = f"RealAudios/{speaker}_recordings"      # path of real audios
    output_dir = f"FakeAudios/{speaker}_recordings"     # path of deepfake audios
    os.makedirs(output_dir, exist_ok=True)
    print(f"Fetching transcripts for {speaker}")
    transcript = fetchTranscript(input_dir)
    jasonifyTranscript(transcript)
    print(f"Saved the transcript in json format for {speaker}")
    print("Creating Deepfake dataset for {speaker}")
    for num, text in transcript.items():


