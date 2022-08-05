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
from playsound import playsound
from flask import send_file

#27017
app = Flask(__name__)
client = MongoClient(hsdef.MONGODB_URI,hsdef.MONGODB_PORT)
hs_movie = client['hsdb']

hsm_requests = hs_movie.hsm_requests
# hsm_requests.delete_many({})


@app.route('/upload')
def render_file():
    # return os.getcwd() /hsapp
    if not os.path.exists('/hsapp/templates'):
        os.mkdir('/hsapp/templates')
        src=os.path.join("/mnt","upload.html")
        target=os.path.join("/hsapp/templates","uploadmnt.html")
        
        shutil.copyfile(src,target)
    
    return render_template('uploadmnt.html')

@app.route('/fileUpload',methods=['GET','POST'])
def upload_file():
    # return str(request.method)
    if request.method=='POST':
        
        f=request.files['file']
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')
        f.save(secure_filename(f.filename))
        saved_file_path=os.path.abspath(f.filename)
        copy_file_path=os.path.join("/tmp",secure_filename(f.filename))
        shutil.copyfile(saved_file_path,copy_file_path) #./tmp/디렉토리에 mp4저장
        
        # db
        req={
            "DIR":hsdef.SRC,
            "FILENAME":f.filename,
            "STATUS": hsdef.PROCESSING,
            "DATETIME": datetime.datetime.now()
        }
        availableFlag=secure_filename(f.filename)[-3:]
        if availableFlag=="mp4":
            req["Avail"]=hsdef.AVAIL
        else:
            req["Avail"]=hsdef.UNAVAIL

        R_id=hs_movie.hsm_requests.insert_one(req).inserted_id
        
        # for d in hs_movie['hsm_requests'].find():
        #     print(d['DIR'], d['FILENAME'], d['STATUS'],d['DATETIME'],d['_id'])
        
        MountReqDir=os.path.join("/mnt/movies",str(R_id))
        os.mkdir(MountReqDir) #Request_ID 디렉토리 생성
        RequestSrcDir=os.path.join(MountReqDir,"Source")
        os.mkdir(RequestSrcDir)

        tmpPathName=secure_filename(f.filename)
        # if availableFlag!="mp4":
        #     while True:
        #         hs_query={"_id":R_id}
        #         hs_doc=hsm_requests.find(hs_query)
        #         flag=0
        #         for d in hs_doc:
        #             if d["Avail"]==hsdef.AVAIL:
        #                 tmpPathName=d["FILENAME"]
        #                 flag=1
        #         if flag==1:
        #             break
        
        fileSrc=os.path.join("/tmp",tmpPathName)
        fileTar=os.path.join("/mnt/movies",str(R_id),"Source",tmpPathName)
        shutil.copyfile(fileSrc,fileTar)
        
        firstResPath=os.path.join("/mnt","resorback.html")
        firstResDir=os.path.join("/hsapp/templates","resorback.html")
        shutil.copyfile(firstResPath,firstResDir)
        
        return render_template("resorback.html",ID=str(R_id))
        # while(1):
        #     htmlpath=os.path.join("/mnt",str(R_id)+".html")
        #     if os.path.exists(htmlpath):
        #         # htmltargetPath=os.path.join("/hsapp/templates",str(R_id)+".html")
        #         # shutil.copyfile(j2path,j2targetPath)
        #         shutil.copyfile(os.path.join("/mnt","mp3test.html"),os.path.join("/hsapp/templates","mp3test.html"))
        #         # return render_template("mp3test.html")
        #         return str(R_id)
        #         # return send_file(os.path.join("/mnt/movies",str(R_id),"Target",str(R_id)+".mp3"),as_attachment=True)
        #         # return send_file(os.path.join("/mnt/movies",str(R_id),"Target",str(R_id)+".mp3"))
        #         # return render_template(str(R_id)+".j2",currentID=str(R_id))
        #         # return playsound(os.path.join("/mnt/movies",str(R_id),"Target",str(R_id)+".mp3"))

@app.route('/result',methods=['GET','POST'])
def result():
    a=os.path.join("/mnt","result.html")
    b=os.path.join("/hsapp/templates","result.html")
    shutil.copyfile(a,b)
    # col_size=hs_movie.hsm_requests.count()
    # print(col_size)
    result_DB=[]
    for d in hs_movie['hsm_requests'].find():
        # print(d['DIR'], d['FILENAME'], d['STATUS'],d['DATETIME'],d['_id'])
        result_DB.append(d)        
    return render_template("result.html",result_DB=result_DB)    
    # return result_DB[0]["FILENAME"]
    # for i in range(len(result_DB)):

@app.route('/<R_id>',methods=['GET','POST'])        
def Download(R_id):
    hs_doc=hsm_requests.find({})
    for to_delete in hs_doc:
        if str(to_delete["_id"])==R_id:
            hs_movie.hsm_requests.update_one({"_id":to_delete["_id"]},{"$set":{"STATUS":hsdef.DELETED}})
            break        
    # hs_movie.hsm_requests.update_one({"_id":ObjectId(R_id)},{"$set":{"STATUS":hsdef.DELETED}})
    return send_file(os.path.join("/mnt/movies",str(R_id),"Target",str(R_id)+".mp3"),as_attachment=True)
    
    
    
        # hsm_requests.delete_one({"_id":toDisplay["_id"]})
    # return "hello"+R_id
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)        
