import streamlit as st
from openai import OpenAI

def format_content_multiple_images(prompt, image_file_ids, type):
    content = []
    text_type = {"type": "text", "text": f"{prompt}"}
    if type == "file_id":
        for image_file_id in image_file_ids:
            image_type_file = {
                "type": "image_file", 
                "image_file": {
                    "file_id": f"{image_file_id}"
                }
            }
            content.append(image_type_file)
    elif type == "file_url_https":
        for image_file_id in image_file_ids:
            image_type_file = {
                "type": "image_url",
                "image_url": {
                    "url": f"{image_file_id}"
                }
            }
            content.append(image_type_file)
    else:
        for image_file_id in image_file_ids:
            image_type_file = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_file_id}"
                }
            }
            content.append(image_type_file)
    content.append(text_type)
    return content
        
   
    
imageurls = ["https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"]
prompt = "afdklsfajd;sfajk;dsfajd;lkfads;lkfja"
a = format_content_multiple_images(prompt, imageurls, "file_url_https")
print(a)