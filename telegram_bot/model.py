import torch
import torchvision.transforms as transforms

from fastai import *

from fastai.vision import *

import PIL

from fastai.vision import image as image_func



class ClassPredictor():
  
  
    def __init__(self):

        self.device = torch.device("cpu")

                
	#loading of model
	self.sz = 200
	tfms = get_transforms(do_flip=False)
        data = ImageDataBunch.from_folder('../art_dataset/', train='training_set', valid='validation_set', ds_tfms=tfms, size=self.sz, num_workers=0)

        learn = create_cnn(data, models.resnet50, metrics=accuracy, model_dir='')

        
self.model = learn.load(name='model', device='cpu')


        
self.transforms = transforms.Compose([

            					transforms.Resize(200),

            					transforms.ToTensor()

        					])



    def predict(self, img_stream):

        img = self.process_image(img_stream)

        self.model.precompute = False
 
       preds = self.model.predict(img)

        return preds[0]



    def process_image(self, img_stream):

        img = PIL.Image.open(img_stream)

        img = self.transforms(img)

        img = image_func.Image(img)

        img = img.set_sample()

        return img
