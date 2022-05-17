import argparse
import json
import pandas as pd
#
# Parse argument
 #parser = argparse.ArgumentParser(prog='transcriber')
 #parser.add_argument('-i', help='Enter the .wav file path')
 #args = parser.parse_args()

 # 1. Read API from text file
f = open("api.txt", "r")
api_key = f.read()
#
print('1. API is read ...')
#
import os
#
# # video = YouTube("https://www.youtube.com/watch?v=mkVjrB8g6mM")
# #video = YouTube(args.i)
# #yt = video.streams.get_audio_only()
#
# #yt.download()
#
current_dir = os.getcwd()

for file in os.listdir(current_dir):
    if file.endswith(".wav"):
        wav_file = os.path.join(current_dir, file)
        # print(mp4_file)
# print('2. Audio file has been retrieved from YouTube video')
#
# # 3. Upload YouTube audio file to AssemblyAI

import sys
import time
import requests

filename = wav_file


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


headers = {'authorization': api_key}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

audio_url = response.json()['upload_url']
#
print('3.  audio file has been uploaded to Server')
#
# # 4. Transcribe uploaded audio file
#
import requests

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
    "audio_url": audio_url,
    "speaker_labels": True,
}

headers = {
    "authorization": api_key,
    "content-type": "application/json"
}

transcript_input_response = requests.post(endpoint, json=json, headers=headers)

print('4. Transcribing uploaded file')

# 5. Extract transcript ID

transcript_id = transcript_input_response.json()["id"]
#
print('5. Extract transcript ID')
#
 # 6. Retrieve transcription results
endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
headers = {
     "authorization": api_key,
 }
#
transcript_output_response = requests.get(endpoint, headers=headers)
#
print('6. Retrieve transcription results')
#
# Check if transcription is complete
from time import sleep
#
while transcript_output_response.json()['status'] != 'completed':

    import pdb;pdb.set_trace()
    sleep(5)
    print('Transcription is processing ...')
    transcript_output_response = requests.get(endpoint, headers=headers)
#
 # print(transcript_output_response.json()["status"])
#
#
 # 7. Print transcribed text
#
print('----------\n')
print('Output:\n')
# print(transcript_output_response.json()["text"])

#yt_txt = open('text.txt', 'w')
#yt_txt.write(transcript_output_response.json()["text"])
#yt_txt.close()
#data=json.load(transcript_output_response)
tempdict={}
final_list=[]
# data = transcript_output_response.json()
# for item in data['words']:
#     if('text' in item ) and ('speaker' in item) and ('confidence' in item):
#         tempdict={'text':item['text'],'speaker':item['speaker'],'confidence':item['confidence']}
#         final_list.append(tempdict)
# #        with open('trancribed_texts', 'w') as fout:
# #             json.dump(final_list,fout)
#
# # print(final_list,'total data')
# # 8. Save transcribed text to file
#
# # Save as TXT file
#
#
#
# # yt_txt.close()
#
# # Save as SRT file
# #srt_endpoint = endpoint + "/srt"
# #srt_response = requests.get(srt_endpoint, headers=headers)
#
# #with open("yt.srt", "w") as _file:
#     #_file.write(srt_response.text)
#
def Excel_as_writer(file):
    df= pd.DataFrame.from_dict(file)
    df.to_excel('Transcribed.xlsx')
#
#
#Excel_as_writer(final_list)
#
#
#
# import spacy
# from spacy import displacy

# NER = spacy.load("en_core_web_sm")

paragraph=endpoint +"/sentences"
para_response=requests.get(paragraph,headers=headers)
# print(para_response.json(),'testtttt')
# print('test')
for sentences in para_response.json()['sentences']:
    if ('text' in sentences) and ('speaker' in sentences) and ('confidence' in sentences):
        # raw_text=sentences['text']
        # text1 = NER(raw_text)
        # for word in text1.ents:
        #     print(word.text, word.label_)
        tempdict = {'text': sentences['text'], 'speaker': sentences['speaker'], 'confidence': sentences['confidence']}
        final_list.append(tempdict)
Excel_as_writer(final_list)



