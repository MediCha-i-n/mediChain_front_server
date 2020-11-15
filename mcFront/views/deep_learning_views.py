from flask import Blueprint, request
from tensorflow.keras.models import model_from_json

from ..deep_learning import update_model

bp = Blueprint('dl', __name__, url_prefix='/dl')

@bp.route('/update_weight/', methods=('GET','POST'))
def update_weight():
    if request.method == 'POST':
        json_data = request.get_json()
        model = model_from_json(json_data)
        ###
        update_model.update(model)
        return "Success"
    else:
        return "fail to update model"
