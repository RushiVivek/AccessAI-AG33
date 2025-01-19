import google.generativeai as genai
import PIL.Image
import requests, io

genai.configure(api_key="AIzaSyAXRaEhq3pgXTktGztOFcDvsB2mfvb3ZSo")
model = genai.GenerativeModel("gemini-1.5-flash")

def getAlt(src):
    try:
        response = requests.get(src)
        image = PIL.Image.open(io.BytesIO(response.content))
        
        response = model.generate_content(["Give alt for this image in less than five words in square brackets", image])
        
        return response.text.split("[")[1].split("]")[0]
        
    except Exception as e:
        return "Image description not available"

def is_suitable_label(label, inp):
    isSuitable = model.generate_content(f"give answers in square brackets, Give True if current label is a suitable label to the input field else give False, Label: {label}; input: {inp}; ")
    return isSuitable.text.split("[")[1].split("]")[0] == "True"

def getLabel(inp, label=""):
    try:
        if label and is_suitable_label(label, inp):
            return 'y'

        prompt = f"give answer in square brackets generate a one or two word label for the input field: {inp}"
        response = model.generate_content(prompt)
        return response.text.split("[")[1].split("]")[0]

    except Exception:
        return ""

def getColors(style):
    try:
        prompt = f"Given the inline style of an element in HTML, give a modified style with text color for the element based on background color, give answer inside square brackets: {style}"
        response = model.generate_content(prompt)

        return response.text.split('[')[1].split("]")[0]

    except Exception as e:
        print(e)

# html_input = {
#     'type': 'text',
#     'placeholder': 'Enter your name'
# }
# existing_label = "UserName"

# suggested_label = getLabel(html_input, existing_label)
# print(suggested_label)

