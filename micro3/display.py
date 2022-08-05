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

def AVI2MP4():
    # find avi(UNAVAIL)
    hs_query={"Avail":hsdef.UNAVAIL}
    hs_doc=hsm_requests.find(hs_query)

    for unAvail in hs_doc:
        filename=unAvail["FILENAME"] #avi
        R_id=str(unAvail["_id"])
        avi_file_path=os.path.join("/mnt/movies",R_id,hsdef.SRC,filename) #avi path
        output_name=os.path.join("/mnt/movies",R_id,hsdef.SRC,filename[:-4]) #mp4 path
        # os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
        # avi->mp4
        os.popen("ffmpeg -fflags +genpts -i '{input}' -c:v copy -c:a copy '{output}.mp4'".format(input = avi_file_path, output = output_name))
        
        #set avail
        hs_movie.hsm_requests.update_one({"_id":unAvail["_id"]},{"$set":{"Avail":hsdef.AVAIL}})
        #set filename avi->mp4
        hs_movie.hsm_requests.update_one({"_id":unAvail["_id"]},{"$set":{"FILENAME":filename[:-4]+".mp4"}})
        
        time.sleep(5) #SOLUTION
        if not os.path.exists(os.path.join("/mnt/movies",R_id,hsdef.SRC,filename[:-4]+".mp4")):
            hs_movie.hsm_requests.update_one({"_id":unAvail["_id"]},{"$set":{"Avail":"format ERROR"}})    
        else:    
            hs_movie.hsm_requests.update_one({"_id":unAvail["_id"]},{"$set":{"Avail":hsdef.AVAIL}})
            hs_movie.hsm_requests.update_one({"_id":unAvail["_id"]},{"$set":{"FILENAME":filename[:-4]+".mp4"}})
        
    time.sleep(5) 
    
    return True

# def FIN2DEL():
#     hs_query={"STATUS":hsdef.FINISHED}
#     hs_doc=hsm_requests.find(hs_query)
#     for toDisplay in hs_doc:
#         R_id=str(toDisplay["_id"])
#         hs_movie.hsm_requests.update_one({"_id":toDisplay["_id"]},{"$set":{"STATUS":hsdef.DELETED}})
#         # hsm_requests.delete_one({"_id":toDisplay["_id"]})
#     time.sleep(5)
if __name__ == "__main__":    
    while True:
        AVI2MP4()

