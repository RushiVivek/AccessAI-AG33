from flask import Flask, request, render_template  
from playwright.sync_api import sync_playwright  
from PIL import Image  
import os  
import numpy as np  
import io  
import concurrent.futures  
import base64  

app = Flask(__name__)  

# Ensure these folders exist  
SCREENSHOTS_FOLDER = "static"  
os.makedirs(SCREENSHOTS_FOLDER, exist_ok=True)  

def take_screenshot(url):  
    """Capture screenshot of a website"""  
    try:  
        with sync_playwright() as p:  
            browser = p.chromium.launch(headless=True)  
            page = browser.new_page(viewport={'width': 1280, 'height': 720})  
            page.goto(url, wait_until='networkidle', timeout=15000)  
            screenshot = page.screenshot(type='png', full_page=True)  
            browser.close()  
            return screenshot  
    except Exception as e:  
        print(f"Screenshot error for {url}: {e}")  
        return None  

def save_screenshot(screenshot_bytes, filename):  
    """Save screenshot to static folder"""  
    if screenshot_bytes:  
        filepath = os.path.join(SCREENSHOTS_FOLDER, filename)  
        with open(filepath, 'wb') as f:  
            f.write(screenshot_bytes)  
        return True  
    return False  

def quick_image_comparison(image1_bytes, image2_bytes):  
    """Fast image comparison"""  
    try:  
        image1 = Image.open(io.BytesIO(image1_bytes)).convert('RGB')  
        image2 = Image.open(io.BytesIO(image2_bytes)).convert('RGB')  
        
        # Resize for faster comparison  
        image1 = image1.resize((300, 300))  
        image2 = image2.resize((300, 300))  
        
        array1 = np.array(image1)  
        array2 = np.array(image2)  
        
        diff = np.abs(array1.astype(np.float32) - array2.astype(np.float32))  
        diff_percentage = (diff.mean() / 255) * 100  
        
        return diff_percentage  
    except Exception as e:  
        print(f"Image comparison error: {e}")  
        return 0  

def rapid_visual_score(image_bytes):  
    """Quick visual quality assessment"""  
    try:  
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')  
        image = image.resize((200, 200))  
        array = np.array(image)  
        
        # Color diversity  
        unique_colors = len(np.unique(array.reshape(-1, 3), axis=0))  
        color_score = min(unique_colors / 1000, 1.0)  
        
        # Contrast  
        grayscale = np.dot(array[...,:3], [0.2989, 0.5870, 0.1140])  
        contrast_score = np.std(grayscale) / 128  
        
        return (color_score * 0.5 + min(contrast_score, 1.0) * 0.5)  
    except Exception as e:  
        print(f"Visual score error: {e}")  
        return 0.5  

@app.route("/", methods=["GET", "POST"])  
def index():  
    if request.method == "POST":  
        original_url = request.form.get("original_url")  
        modified_url = request.form.get("modified_url")  

        # Capture screenshots  
        with concurrent.futures.ThreadPoolExecutor() as executor:  
            original_screenshot = executor.submit(take_screenshot, original_url)  
            modified_screenshot = executor.submit(take_screenshot, modified_url)  
            
            original_screenshot = original_screenshot.result()  
            modified_screenshot = modified_screenshot.result()  

        if not (original_screenshot and modified_screenshot):  
            return render_template("comparePictures.html", error="Failed to capture screenshots")  

        # Save screenshots  
        save_screenshot(original_screenshot, 'original_screenshot.png')  
        save_screenshot(modified_screenshot, 'modified_screenshot.png')  

        # Parallel analysis  
        with concurrent.futures.ThreadPoolExecutor() as executor:  
            original_score = executor.submit(rapid_visual_score, original_screenshot)  
            modified_score = executor.submit(rapid_visual_score, modified_screenshot)  
            diff_percentage = executor.submit(quick_image_comparison, original_screenshot, modified_screenshot)  
            
            original_score = original_score.result()  
            modified_score = modified_score.result()  
            diff_percentage = diff_percentage.result()  

        # Determine comparison result  
        if original_score > modified_score:  
            result = f"Original website is visually better. Score: {original_score:.2f} vs {modified_score:.2f}"  
        elif modified_score > original_score:  
            result = f"Modified website is visually better. Score: {modified_score:.2f} vs {original_score:.2f}"  
        else:  
            result = "Both websites have similar visual quality"  

        return render_template("comparePictures.html",   
                               result=result,  
                               diff_percentage=diff_percentage,  
                               original_score=original_score,  
                               modified_score=modified_score)  

    return render_template("comparePictures.html")  

if __name__ == "__main__":  
    # Install playwright browsers first time  
    import sys  
    import subprocess  
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])  
    
    app.run(debug=True)