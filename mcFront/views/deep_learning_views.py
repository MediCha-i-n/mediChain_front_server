from flask import Blueprint, request
from tensorflow.keras.models import model_from_json

from ..deep_learning import predict, Unet

bp = Blueprint('dl', __name__, url_prefix='/dl')

@bp.route('/update_weight/', methods=('GET','POST'))
def update_weight():
    if request.method == 'POST':
        data = request.get_json()
        model = data.model_from_json(data)

        ###
        model.save("best_model.hdf5")
