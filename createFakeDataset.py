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

def trainOnAudioPhile(speaker, philenum):
    input_file_path = os.path.join(input_dir, f"{speaker}_input{philenum}.wav")
    target_se, audio_name = se_extractor.get_se(input_file_path, tone_color_converter, vad=True)

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
        try:
            trainOnAudioPhile(speaker, num)
        except: # there were errors of audio being too short as it was randomly trimmed, when I was running testing it on jupyter notebook
            if num!=1:
                trainOnAudioPhile(speaker, num-1)
            trainOnAudioPhile(speaker, num+1)
        try:
            model = TTS(language=language, device=device)
            tmp_path = os.path.join(output_dir, "tmp.wav")
            model.tts_to_file(text, speaker_id, tmp_path, speed=speed)
    
            output_file = os.path.join(output_dir, f"{speaker}_output{num}.wav")
    
            encode_message = "@MyShell"
            tone_color_converter.convert(
                audio_src_path=tmp_path,
                src_se=source_se,
                tgt_se=target_se,
                output_path=output_file,
                message=encode_message
            )
        
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
            print(f"Processed input {num}: output saved to {output_file}")
        except:
            error_message = traceback.format_exc()
            with open(log_file_path, "a") as log_file:
                log_file.write(f"Error processing file {speaker}_input{num}.wav:\n{error_message}\n")
            print(f"Error processing file {speaker}_input{num}.wav: {str(e)}")
