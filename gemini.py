import google.generativeai as genai
import PIL.Image
import requests, io

genai.configure(api_key="AIzaSyAXRaEhq3pgXTktGztOFcDvsB2mfvb3ZSo")
model = genai.GenerativeModel("gemini-1.5-flash")

def getAlt(src):
    try:
        response = requests.get(src)
        image = PIL.Image.open(io.BytesIO(response.content))
        
        response = model.generate_content(["Give alt text for this image in less than 20 letters", image])
        
        return response.text
        
    except Exception as e:
        return "Image description not available"
