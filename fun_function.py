
#importing libraries from transformers , for encoding and feature extracting , tokenizing ,and take data from pretrained data hugging face
from transformers import VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
import torch
from PIL import Image

#pip install transformers (already installed in anaconda prompt, so need of installing)

#It consists of two main parts: an encoder that processes images and a decoder that generates text. 
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

#ViTFeatureExtractor is a tool that helps prepare images for use with a Vision Transformer (ViT) model
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

#it removes unwanted stop words in text
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# if we have gpu than run on gpu other wise run on cpu only

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def predict_step(image_path, num_captions=3, max_length=25, num_beams=4):
    images = []
    for i in range(num_captions):
        i_image = Image.open(image_path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")
        images.append(i_image)
     
    #The "model.generate" method is called to generate captions for the given images. It takes several arguments:
    
    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(
        pixel_values,
        do_sample=True,
        num_return_sequences=num_captions,
        max_length=max_length,
        num_beams=num_beams,
        temperature=1.0,
        top_p=0.9,
        top_k=0,
        
        #The token ID used for padding the captions.
        
        ## The token ID used to indicate the start of the caption.
        
        pad_token_id=tokenizer.pad_token_id,
        
        
        
        decoder_start_token_id=tokenizer.cls_token_id
    )

    captions = []
    for i in range(num_captions):
        preds = tokenizer.decode(output_ids[i], skip_special_tokens=True)
        captions.append(preds.strip())

    return captions




def fun(image_path):
    
    num_captions = 3
    captions = predict_step(image_path, num_captions=num_captions)
    return captions





