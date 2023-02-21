import numpy as np
import torch
import torchvision as tv
from flask import Flask, request, render_template
from PIL import Image, ImageOps
from med import MedNet


# Charger le modèle en mémoire
model = torch.load('model/saved_model.pt', map_location=torch.device('cpu'))

def scaleImage(y):          # Pass a PIL image, return a tensor
    if(y.min() < y.max()):  # Assuming the image isn't empty, rescale so its values run from 0 to 1
        y = (y - y.min())/(y.max() - y.min()) 
    z = y - y.mean()        # Subtract the mean value of the image
    return z


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apply_model', methods=['POST'])
def apply_model():
    # Récupérer l'image depuis le formulaire
    image_file = request.files['image']
    image = Image.open(image_file.stream)
    
    # Transforme en gris
    image = ImageOps.grayscale(image)

    # Resize
    size = 64, 64
    image = image.resize(size)

    toTensor = tv.transforms.ToTensor()
    image = toTensor(image)

    #Reshape for the model
    image = image.reshape([1,1,64,64])
    image=scaleImage(image) 
    classname = ['AbdomenCT', 'BreastMRI', 'ChestCT', 'CXR', 'Hand', 'HeadCT']
    yOut = model(image)
    max=yOut.max(1)[1].tolist()[0]
    pred=classname[max]
    return pred

    # # Prétraiter l'image et effectuer la prédiction
    # with torch.no_grad():
    #     y = model(image)
    #     prediction = torch.argmax(y)
    
    # # Renvoyer le résultat de la prédiction
    # return str(prediction.item())

if __name__ == '__main__':
    app.run()

