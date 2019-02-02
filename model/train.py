import numpy as np
import pandas as pd
import os

# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

from fastai import *
from fastai.vision import *

data_dir = './art_dataset/'
model_dir = './models/'
sz=200

tfms = get_transforms(do_flip=False)
data = ImageDataBunch.from_folder(data_dir, train='training_set', valid='validation_set', ds_tfms=tfms, size=sz, num_workers=0)

learn = create_cnn(data, models.resnet50, metrics=accuracy, model_dir=model_dir)

learn.fit_one_cycle(23,1e-2)
# learn.recorder.plot()

learn.save('model')