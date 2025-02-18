import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter
from transcript import *
from melo.api import TTS

input_dir = f"RealAudios/{speaker}_recordings"      # path of real audios
output_dir = f"FakeAudios/{speaker}_recordings"     # path of deepfake audios
# os.makedirs(output_dir, exist_ok=True)

parento = "./RealAudios"
speakeros = []
for folderName in os.listdir(parento):
    folderPath = os.path.join(parento, folderName)
    if os.path.isdir(folderPath) and folderName.startswith('speaker'):
        speakeros.append(folderName)


