from flask import Blueprint, request, render_template, url_for, g, flash
from werkzeug.utils import redirect
from werkzeug.datastructures import FileStorage
import subprocess
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
from ..urls import blockchain_api_url

bp = Blueprint('act', __name__, url_prefix='/act')

@bp.route('/search/', methods=('GET','POST'))
@login_required
def search():
    form = ActSearchForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        patientHash = form.patientHash.data
        if g.user.docAuth or g.user.patientHash == patientHash:
            blockchain_url = blockchain_api_url()
            if g.user.docAuth:
                apiURL = blockchain_url + 'doctor/getPatientData/trainer'
                print("This is ========", apiURL)
            else:
                apiURL = blockchain_url + 'doctor/patient/getMyData/trainer'
            params = {'patientHash': patientHash}
            response = requests.get(apiURL, params=params)

##################################################################################################################
##################################################################################################################

            # response = '''[
            #  {
            #     "TxId": "dd6d392f350e74a027fed8fdf68e88802dea590ec6db33990ca7e423ba594c51",
            #     "Timestamp": {
            #         "seconds": { "low": 1600792773, "high": 0, "unsigned": "false" },
            #         "nanos": 449000000
            #     },
            #     "Value": {
            #         "doctorNumber": "0",
            #         "enrollNumber": 179,
            #         "patientHash": "trainer 3",
            #         "rawImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly",
            #         "resultImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly"
            #     }
            #   },
            #   {
            #     "Timestamp": {
            #         "seconds": { "low": 1600792890, "high": 0, "unsigned": "false" },
            #         "nanos": 449000000
            #     },
            #     "Value": {
            #       "doctorID": "doctor",
            #       "enrollNumber": 2,
            #       "patientHash": "patientHash1",
            #       "rawImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly",
            #       "resultImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly"
            #     }
            #   },
            #   {
            #     "Timestamp": {
            #         "seconds": { "low": 1608799999, "high": 0, "unsigned": "false" },
            #         "nanos": 449000000
            #     },
            #     "Value": {
            #       "patientHash": "patientHash1",
            #       "enrollNumber": 1,
            #       "doctorID": "doctor",
            #       "rawImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly",
            #       "resultImgCID": "bafybeihpi4cthvkkh7x6oy3ozxo3x6w46iyazn5u4wrxjiy2twxywkraly"
            #     }
            #   }
            # ]
            # '''

##################################################################################################################
##################################################################################################################

            # print("Response Type: ", type(response))
            # print("Response: ", response)
            # print("Response Headers: ", response.headers)
            # print("Response Text: ", response.text)
            data_list = []
            json_res = json.loads(response.text)
            if "message" in json_res and json_res["message"] == "Not exist patientHash":
                error = "등록되지 않은 해쉬입니다."
            else:
                res = sorted(json_res, key=lambda x: -(x['Timestamp']['seconds']['low']))
                # res = sorted(response.json(), key=lambda x: -(x['Timestamp']['seconds']['low']))
                for each_data in res:
                    tm = time.localtime(each_data['Timestamp']['seconds']['low'])
                    time_data = str(tm.tm_year) + '.' + str(tm.tm_mon) + '.' + str(tm.tm_mday) + ' / ' + str(tm.tm_hour) + ':' + str(tm.tm_min)
                    rawImg_location = "https://" + each_data['Value']['rawImgCID'] + ".ipfs.cf-ipfs.com/"
                    resultImg_location = "https://" + each_data['Value']['resultImgCID'] + ".ipfs.cf-ipfs.com/"
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
        # image_length = image.content_length   #   This is 0.
        image_file = image.read()
        sha256_hash = hashlib.sha256(form.patientHash.data.encode())
        patientHash = sha256_hash

        ####
        # test_code = ipfshttpclient.connect()
        # print(test_code.id())
        ####

        # print(patientHash)
        encoded_file = base64.b64encode(image_file)
        # print(encoded_file)

        ### File upload to IPFS ###
        tmp_file_name = str(g.user.doctorNumber)+".jpg"
        with open(tmp_file_name, "wb") as tmp_file:
            tmp_file.write(base64.b64decode(encoded_file))
        ipfs_api = ipfsApi.Client("127.0.0.1", 5001)
        ipfs_response = ipfs_api.add(tmp_file_name)
        img_cid = ipfs_response["Hash"]
        os.remove(tmp_file_name)
        # print(ipfs_response)
        ###########################

        blockchain_url = blockchain_api_url()
        apiURL = blockchain_url + '/doctor/uploadPatientData'
        # data = {
        #     "doctorNumber": g.user.doctorNumber,
        #     "patientHash": patientHash,
        #     "rawImgCID": img_cid,
        #     #####     TEST CODE   ########
        #     "resultImgCID": "",
        # }
        # response = requests.post(apiURL, data=data)

        # print("Response Type: ", type(response))
        # print("Response: ", response)
        # print("Response Headers: ", response.headers)
        # print("Response Text: ", response.text)
        data_list = []
        # res = sorted(json.loads(response.text), key=lambda x: -(x['Timestamp']['seconds']['low']))
        # for each_data in res:
        #     tm = time.localtime(each_data['Timestamp']['seconds']['low'])
        #     time_data = {'year': tm.tm_year, 'month': tm.tm_mon, 'day': tm.tm_mday, 'hour': tm.tm_hour,
        #                  'minute': tm.tm_min}
        #     data = {'time': time_data, 'rawImgCID': each_data['Value']['rawImgCID'],
        #             'resultImgCID': each_data['Value']['resultImgCID']}
        #     data_list.append(data)
        return render_template('act/showResult.html', data_list=data_list)

    return render_template('act/upload.html', form=form)

