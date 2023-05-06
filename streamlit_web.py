
import streamlit as st
from fun_function import fun


st.title("Image Caption Generator")


def validate_file(file):
    if file is None:
        st.warning("Please upload an image.")
        return False
    elif not file.type.startswith("image"):
        st.warning("Please upload an image file.")
        return False
    else:
        return True

#Streamlit file uploader widget
file = st.file_uploader("Upload file", type=["jpg", "jpeg", "png"])




    
if validate_file(file):
    file_name = file.name
    image = file.read()
    captions = fun(file_name) 
    st.image(image, use_column_width=True)
    st.title("-:Captions:-")
    for caption in captions:
        
        st.write(caption)
    
    

