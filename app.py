from flask import Flask,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask_cors import CORS

###initialize git
#url https://ansoryapi.herokuapp.com/
app = Flask(__name__)
CORS(app)
##heroku
# cred = credentials.Certificate('ansory-8dc38-firebase-adminsdk-2xtx8-de4e743e1b.json')
##python anywhere
cred = credentials.Certificate('/home/syihabuddin/mysite/ansory-8dc38-firebase-adminsdk-2xtx8-de4e743e1b.json')
firebase_admin.initialize_app(cred)
dbq = firestore.client()
doc_ref = dbq.collection('datasiswa')
tbl_nilai = dbq.collection('testresult')

@app.route('/login',methods=["POST"])
def login():
    data = request.form.to_dict(flat=False)
    val = doc_ref.where("username","==",data['username'][0]).where("pass","==",data['pass'][0]).get()
    if (len(val) == 1):
        return {"data" : "sukses","nama":val[0].to_dict()['nama siswa'],"kelas":val[0].to_dict()['kelas'],"absen" :val[0].to_dict()['absen'],"username":val[0].to_dict()['username'], "id" : val[0].id}
    else:
        return{"data":"password atau username salah"}

@app.route("/getdatasiswa")
def getdatasiswa():
    data = doc_ref.get()
    dataNilai = tbl_nilai.get()
    djson = []
    for i in range(len(data)):
        nama = data[i].to_dict()['nama siswa']
        kelas = data[i].to_dict()['kelas']
        absen = data[i].to_dict()['absen']
        username = data[i].to_dict()['username']
        ids = data[i].id
        if(len(dataNilai) == 0):
            djson.append({"nama" : nama,'absen' : absen,'kelas' : kelas,"id":"","username":username,"nilai" : "belum tes","idsiswa": ids})
        else:
            flag = 0
            for j in range(len(dataNilai)):
                if(data[i].to_dict()['username'] == dataNilai[j].to_dict()['username']):
                    flag = 1
                    djson.append({"nama" : nama,'absen' : absen,'kelas' : kelas,"id":dataNilai[j].id,"username":username,"nilai" : dataNilai[j].to_dict()['nilai'],"idsiswa": ids})
                    break
            if(flag == 0):
                djson.append({"nama" : nama,'absen' : absen,'kelas' : kelas,"id":"","username":username,"nilai" : "belum tes","idsiswa": ids})
            
    return{"data":djson}

@app.route("/register",methods=["POST"])
def register():
    data = request.form.to_dict(flat=False)
    val = doc_ref.where("username","==",data['username'][0]).get()
    # print(len(val))
    if(len(val)==0):
        doc_ref.document().set({
            'absen':data['absen'][0],
            'kelas':data['kelas'][0],
            'nama siswa':data['nama siswa'][0],
            'pass':data['pass'][0],
            'username':data['username'][0],
        })
        valz = doc_ref.where("username","==",data['username'][0]).get()
        for i in range(len(valz)):
            ids = valz[i].id
        return{"data":"sukses","id" :ids}
    else:
        return{"data":"username telah diambil"}

@app.route("/insertnilai",methods=["POST"])
def insertnilai():
    data = request.form.to_dict(flat=False)
    val = tbl_nilai.where("username","==",data['username'][0]).get()
    if(len(val)==0):
        tbl_nilai.document().set({
            'username' : data['username'][0],
            'nilai' : data['nilai'][0]
        })
        return {"data" : "sukses"}
    else :
        return {"data":"anda sudah mengerjakan test !"}

@app.route("/getuserdata",methods=["POST"])
def getuserdata():
    data = request.form.to_dict(flat=False)
    val = doc_ref.where("username","==",data['username'][0]).get()
    dataNilai = tbl_nilai.where("username","==",data['username'][0]).get()
    djson = []
    if(len(dataNilai) == 0):
         for i in range(len(val)):
            nama = val[i].to_dict()['nama siswa']
            kelas = val[i].to_dict()['kelas']
            absen = val[i].to_dict()['absen']
            username = val[i].to_dict()['username']
            ids = val[i].id
            djson.append({"nama" : nama,'absen' : absen,'kelas' : kelas,"id":ids,"username":username,"nilai" : "belum tes"})
    else:
        for i in range(len(val)):
            nama = val[i].to_dict()['nama siswa']
            kelas = val[i].to_dict()['kelas']
            absen = val[i].to_dict()['absen']
            username = val[i].to_dict()['username']
            ids = val[i].id
            nil = dataNilai[i].to_dict()['nilai']
            djson.append({"nama" : nama,'absen' : absen,'kelas' : kelas,"id":ids,"username":username,"nilai" : nil})
    return{"data":djson}

@app.route("/deletenilai",methods=["POST"])
def deletenilai():
    data = request.form.to_dict(flat=False)
    tbl_nilai.document(data['id'][0]).delete()
    val = tbl_nilai.where("username","==",data['username'][0]).get()
    if(len(val)> 0):
        for i in range(len(data)):
            ids = data[i].id
            if(ids == data['id'][0]):
                return {"data" : "gagal dihapus coba lagi !"}
    return {"data":"berhasil dihapus"}

@app.route("/deletesiswa",methods=["POST"])
def deletesiswa():
    data = request.form.to_dict(flat=False)
    doc_ref.document(data['id'][0]).delete()
    val = doc_ref.where("username","==",data['username'][0]).get()
    if(len(val)> 0):
        for i in range(len(data)):
            ids = data[i].id
            if(ids == data['id'][0]):
                return {"data" : "gagal dihapus coba lagi !"}
    return {"data":"berhasil dihapus"}

if __name__ == "__main__":
    app.run(debug=True,)