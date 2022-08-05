from crypt import methods
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import os.path
import shutil
from pymongo import MongoClient
import pymongo
import datetime
import sys
sys.path.append('../hslib')
sys.path.append('../hsdef')
import hsdef as hsdef
import hslib as hslib
from moviepy.editor import *
import time

client = MongoClient(hsdef.MONGODB_URI,hsdef.MONGODB_PORT)
hs_movie = client['hsdb']
hsm_requests = hs_movie.hsm_requests



def mp4tomp3():
    # query processing && available
    hs_query={"STATUS":hsdef.PROCESSING,"Avail":hsdef.AVAIL}
    hs_doc=hsm_requests.find(hs_query)
    
    for toConvert in hs_doc:
        #find dir
        R_id=str(toConvert["_id"])
        
        #mp4 path
        mp4_name=toConvert["FILENAME"]
        mp4_file_path = os.path.join("/mnt/movies",R_id,hsdef.SRC,mp4_name)

        #mp3 path
        mp3_name=R_id+".mp3"
        mp3_file_path=os.path.join("/mnt/movies",R_id,hsdef.TG,mp3_name)
        if not os.path.exists(os.path.join('/mnt/movies',R_id,hsdef.TG)):
            os.mkdir(os.path.join('/mnt/movies',R_id,hsdef.TG))

        #mp4tomp3
        videoclip = VideoFileClip(mp4_file_path)
        if not os.path.exists(mp3_file_path):
            audioclip = videoclip.audio
            audioclip.write_audiofile(mp3_file_path)
            audioclip.close()
        videoclip.close()

        #DB status Update
        if not os.path.exists(mp3_file_path):
            hs_movie.hsm_requests.update_one({"_id":toConvert["_id"]},{"$set":{"STATUS":"mp4 to mp3 err"}})    
        else:
            hs_movie.hsm_requests.update_one({"_id":toConvert["_id"]},{"$set":{"STATUS":hsdef.FINISHED}})
            hs_movie.hsm_requests.update_one({"_id":toConvert["_id"]},{"$set":{"DIR":mp3_file_path}})
    time.sleep(5)

while True:
    mp4tomp3()

# if __name__ == "__main__":
    
        
