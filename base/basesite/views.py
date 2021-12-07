from django.shortcuts import render
from django.conf import settings
import os
# Create your views here.
#rander for HTML file call
from django.shortcuts import render
#HttpResponse For Response code
from django.http import HttpResponse
#use for file heandling
from django.core.files.storage import FileSystemStorage

# Create your test.
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.applications.xception import Xception
from keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import argparse





def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3] 
        image = np.expand_dims(image, axis=0)
        image = image/127.5
        image = image - 1.0
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    return in_text
# Create your test.







# Create your views here.



def home(request):
    return render(request,'pages/home.html')


def bot(request):
    """Process images uploaded by users upload in the Media file"""
    #Store in file
    fileObj = request.FILES['pic']
    
    fs=FileSystemStorage()
    #save and Store in media file
    imgPath=fs.save(fileObj.name,fileObj)
    #save address in media file
    
    imgPath=fs.url(imgPath)
    

    imgoff="."+imgPath
 
    print(imgoff)

 
    



    #save address in media file





    
    max_length = 32
    tokenizer = load(open("models/tokenizer.p","rb"))
    model = load_model('models/model_9.h5')
    xception_model = Xception(include_top=False, pooling="avg")
    

    photo = extract_features(imgoff, xception_model)
    img = Image.open(imgoff)

    description = generate_desc(model, tokenizer, photo, max_length)
    print(description)

    context={'imgPath':imgPath, 'description':description}
    return render(request,'pages/application.html',context)


    



def note(request):
    return render(request,'pages/note.html')
def contact(request):
    
    return render(request,'pages/contact.html')


