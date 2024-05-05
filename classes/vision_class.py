import streamlit as st
from openai import OpenAI
import base64


class VisionAssistant():
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets.openai.api_key)
        self.model = "gpt-4-turbo"
        self.content = []
        self.query = None

    def get_content_text(self, prompt):
        self.content_text = {"type": "text", "text": f"{prompt}"}
        self.content.append(self.content_text)

    def get_image_object(self, image_path):
        base64_image = self.encode_image(image_path=image_path)
        image_object = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        self.content.append(image_object)

    def get_image_objects(self, image_paths):
        for image_path in image_paths:
            self.get_image_object(image_path=image_path)

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def get_content(self, prompt: str=None, image_paths=None):
        if prompt is not None:
            self.get_content_text(prompt=prompt)
        if image_paths is not None:
            self.get_image_objects(image_paths=image_paths)

        self.get_completion()
        print(self.assistant_response)

    def get_completion(self):
        self.response = self.client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": self.content}] )
        self.assistant_response = self.response.choices[0].message.content


#prompt = "Evaluate the images provided and provide a best guess at the application name and description in which they are used."
#imagepaths = ["images/header.png", "images/header1.png", "images/header2.png", "images/header4.png"]
#vasst = VisionAssistant()
#vasst.get_content(prompt=prompt, image_paths=imagepaths)
