import os

def update(model):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model.save(os.path.join(BASE_DIR, "best_model.hdf5"))