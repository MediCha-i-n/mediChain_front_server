from flask import Blueprint, request, render_template, url_for, g, flash
from werkzeug.utils import redirect
from werkzeug.datastructures import FileStorage
from PIL import Image
import subprocess
import numpy as np
import base64
import requests
import time
import json
import ipfsApi
import ipfshttpclient
import os
import hashlib

from mcFront import db
from mcFront.model import Patient, Doctor
from mcFront.forms import ActSearchForm, ActUploadForm
from ..views.auth_views import login_required, docLogin_required
from ..deep_learning import predict
from ..urls import blockchain_api_url

bp = Blueprint('act', __name__, url_prefix='/act')

@bp.route('/search/', methods=('GET','POST'))
@login_required
def search():
    form = ActSearchForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        patientHash = hashlib.sha256(form.patientHash.data.encode()).hexdigest()
        if g.user.docAuth or g.user.patientHash == patientHash:
            blockchain_url = blockchain_api_url()
            if g.user.docAuth:
                apiURL = blockchain_url + 'doctor/getPatientData/' + patientHash
            else:
                apiURL = blockchain_url + 'patient/getMyData/' + patientHash
            response = requests.get(url=apiURL)
            # print("======== TEST ==============")
            # print(response)
            # print(response.text)
            # print("======== TEST ==============")
            # json_res = requests.get(apiURL, params=params).json()

##################################################################################################################
##################################################################################################################

            # response = '''[
            #              {
            #                 "TxId": "dd6d392f350e74a027fed8fdf68e88802dea590ec6db33990ca7e423ba594c51",
            #                 "Timestamp": {
            #                     "seconds": { "low": 1600792773, "high": 0, "unsigned": "false" },
            #                     "nanos": 449000000
            #                 },
            #                 "Value": {
            #                     "doctorNumber": "0",
            #                     "enrollNumber": 179,
            #                     "patientHash": "trainer 3",
            #                     "rawImgCID": "bafybeibyfeyxnyfhychpbnx6hle34mt7hrhwm6dvdy4odgsyqmeayc6jiq",
            #                     "resultImgCID": "bafybeib66h4cpp27wpbt3zhxf3eb5ri6cgvosis7465h4zg5tl3mkdqaj4"
            #                 }
            #               }
            #
            #             ]
            #             '''

##################################################################################################################
##################################################################################################################

            # print("Response Type: ", type(response))
            # print("Response: ", response)
            # print("Response Headers: ", response.headers)
            # print("Response Text: ", response.text)


            data_list = []
            json_res = json.loads(response.text)
            # json_res = json.loads(response)
            # print("============= THIS is json_res ================")
            # print(json_res)
            if "message" in json_res and json_res["message"] == "Not exist patientHash":
                error = "등록되지 않은 해쉬입니다."
            else:
                res = sorted(json.loads(response.text), key=lambda x: -(x['Timestamp']['seconds']['low']))
                for each_data in res:
                    tm = time.localtime(each_data['Timestamp']['seconds']['low'])
                    time_data = str(tm.tm_year) + '.' + str(tm.tm_mon) + '.' + str(tm.tm_mday) + ' / ' + str(
                        tm.tm_hour) + ':' + str(tm.tm_min)
                    # rawImg_location = "https://ipfs.io/ipfs/" + each_data['Value']['rawImgCID'] + "/"
                    rawImg_location = "http://127.0.0.1:8080/ipfs/" + each_data['Value']['rawImgCID'] + "/"
                    # resultImg_location = "https://ipfs.io/ipfs/" + each_data['Value']['resultImgCID'] + "/"
                    resultImg_location = "http://127.0.0.1:8080/ipfs/" + each_data['Value']['resultImgCID'] + "/"
                    data = {'time': time_data, 'rawImg': rawImg_location,
                            'resultImg': resultImg_location}
                    data_list.append(data)

        else:
            error = "해쉬가 환자 정보와 일치하지 않습니다."
        if error is None:
            return render_template('act/showResult.html', data_list=data_list)
        flash(error)
    return render_template('act/search.html', form=form)

@bp.route('/upload/', methods=('GET','POST'))
@docLogin_required
def upload():
    form = ActUploadForm()
    if request.method == 'POST' and form.validate_on_submit():
        image = form.image.data
        image_file = image.read()
        # sha256_hash = hashlib.sha256(form.patientHash.data.encode())
        # patientHash = sha256_hash.hexdigest()

        patientHash = hashlib.sha256(form.patientHash.data.encode()).hexdigest()

        encoded_file = base64.b64encode(image_file)

        ### File upload to IPFS ###
        tmp_file_name = str(g.user.doctorNumber)+".jpg"
        with open(tmp_file_name, "wb") as tmp_file:
            tmp_file.write(base64.b64decode(encoded_file))

        # Unable for awhile
        ### Produce a new image from deep learning model
        new_file_name = "new" + tmp_file_name
        img = Image.open(tmp_file_name)
        pixel_img = np.array(img)
        predicted_img = predict.predict(pixel_img)
        new_image = Image.fromarray(predicted_img)
        new_image = new_image.convert("RGB")
        new_image.save(new_file_name)

        # current_path = os.getcwd()
        # new_file_name = "new_file.tif"

        ipfs_api = ipfsApi.Client("127.0.0.1", 5001)
        ipfs_response = ipfs_api.add(tmp_file_name)
        ipfs_new_response = ipfs_api.add(new_file_name)
        img_cid = ipfs_response["Hash"]
        new_img_cid = ipfs_new_response["Hash"]
        # print("img_cid :",img_cid)

        os.remove(tmp_file_name)

        #######     TEST    #########
        # os.remove(new_file_name)
        # print("ipfs response :", ipfs_response)
        # print("ipfs new response :", ipfs_new_response)
        ###########################

        blockchain_url = blockchain_api_url()
        apiURL = blockchain_url + 'doctor/uploadPatientData'
        # print("apiURL :", apiURL)
        headers = {"Content-Type": "application/json"}
        json_data = {
            "doctorNumber": g.user.doctorNumber,
            "patientHash": patientHash,
            "rawImgCID": img_cid,
            "resultImgCID": new_img_cid
        }
        response = requests.post(url=apiURL, headers=headers, json=json_data)
        # print("Response: ", response)
        # print("Response Headers: ", response.headers)
        # print("Response Text: ", response.text)

        #### Search after upload ####
        apiURL = blockchain_url + 'patient/getMyData/' + patientHash
        response = requests.get(apiURL)
        # print("Response Type: ", type(response))
        # print("Response: ", response)
        # print("Response Headers: ", response.headers)
        # print("Response Text: ", response.text)

        data_list = []
        res = sorted(json.loads(response.text), key=lambda x: -(x['Timestamp']['seconds']['low']))
        for each_data in res:
            tm = time.localtime(each_data['Timestamp']['seconds']['low'])
            time_data = str(tm.tm_year) + '.' + str(tm.tm_mon) + '.' + str(tm.tm_mday) + ' / ' + str(
                tm.tm_hour) + ':' + str(tm.tm_min)
            # rawImg_location = "https://ipfs.io/ipfs/" + each_data['Value']['rawImgCID'] + "/"
            rawImg_location = "http://127.0.0.1:8080/ipfs/" + each_data['Value']['rawImgCID'] + "/"
            # resultImg_location = "https://ipfs.io/ipfs/" + each_data['Value']['resultImgCID'] + "/"
            resultImg_location = "http://127.0.0.1:8080/ipfs/" + each_data['Value']['resultImgCID'] + "/"
            data = {'time': time_data, 'rawImg': rawImg_location,
                    'resultImg': resultImg_location}
            data_list.append(data)
        return render_template('act/showResult.html', data_list=data_list)

    return render_template('act/upload.html', form=form)

