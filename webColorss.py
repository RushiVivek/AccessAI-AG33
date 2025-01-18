import requests  
from bs4 import BeautifulSoup  
import re  
import cssutils  
from gemini import getColors

# Function to parse color from different formats  
def parse_color(color_str):  
    # Remove quotes and whitespace  
    color_str = color_str.strip().strip("'\"")  
    return color_str  

def get_colors(url, soup):  
    # Store color information  
    color_info = []  
    

    # 1. Check inline styles  
    for element in soup.find_all(style=True):  
        inline_style = element.get('style', '')  
        text_color_match = re.search(r'color:\s*([^;]+)', inline_style)  
        bg_color_match = re.search(r'background-color:\s*([^;]+)', inline_style)  
        
        if text_color_match or bg_color_match:  
            # print(element)
            changed_style = getColors(element['style'])
            element['style'] = changed_style
            # spl = element['style'].split("color:")
            # spl = ";".join(spl[1].split(";")[1:])
            # element['style'] = "".join(spl)
            # element['style'] += f'color: {changed_text_color};'
            # color_info.append({  
            #     'type': 1,
            #     'element': element,  
            #     'text_color': parse_color(text_color_match.group(1)) if text_color_match else None,  
            #     'bg_color': parse_color(bg_color_match.group(1)) if bg_color_match else None  
            # })
    


    # 2. Extract colors from CSS stylesheets  
    # style_tags = soup.find_all('style')  
    # link_tags = soup.find_all('link', rel='stylesheet')  
    
    # # Parse CSS from style tags  
    # for style_tag in style_tags:  
    #     css = style_tag.string  
    #     if css:  
    #         color_info.extend(parse_css_colors(css))  
    
    # # Fetch and parse external stylesheets  
    # for link in link_tags:  
    #     href = link.get('href')  
    #     if href:  
    #         # Handle relative URLs  
    #         if not href.startswith(('http://', 'https://')):  
    #             href = requests.compat.urljoin(url, href)  
            
    #         try:  
    #             css_response = requests.get(href)  
    #             color_info.extend(parse_css_colors(css_response.text))  
    #         except Exception as e:  
    #             print(f"Error fetching stylesheet {href}: {e}")  
    
    return color_info  

def parse_css_colors(css_text):  
    color_info = []  
    
    try:  
        # Parse CSS  
        stylesheet = cssutils.parseString(css_text)  
        
        # Iterate through all rules  
        for rule in stylesheet:  
            if rule.type == rule.STYLE_RULE:  
                text_color = None  
                bg_color = None  
                
                # Check for color properties  
                for prop in rule.style:  
                    if prop.name == 'color':  
                        text_color = prop.value  
                    elif prop.name == 'background-color':  
                        bg_color = prop.value  
                
                # If colors found, add to color info  
                if text_color or bg_color:  
                    color_info.append({  
                        'type': 2,
                        'selector': rule.selectorText,  
                        'text_color': text_color,  
                        'bg_color': bg_color  
                    })  
    except Exception as e:  
        print(f"Error parsing CSS: {e}")  
    
    return color_info  

def luminance(color):  
    # Convert color to RGB  
    if color.startswith('#'):  
        color = color.lstrip('#')  
        # Handle different length hex colors  
        if len(color) == 3:  
            color = ''.join([c*2 for c in color])  
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16)  
    elif color.startswith('rgb'):  
        # Parse rgb() or rgba()  
        nums = re.findall(r'\d+', color)  
        r, g, b = map(int, nums[:3])  
    else:  
        # For named colors or unsupported formats  
        return 0.5  
    
    # Standard RGB to luminance conversion
    r = r / 255  
    g = g / 255  
    b = b / 255  
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4  
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4  
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4  
    return 0.2126 * r + 0.7152 * g + 0.0722 * b  

def check_contrast(text_color, background_color):  
    # Note: This is a placeholder. You'd need to implement actual contrast calculation  
    # Using a simple luminance-based contrast calculation  

    try:  
        # Calculate relative luminance and contrast ratio  
        l1 = luminance(text_color)  
        l2 = luminance(background_color)  
        contrast = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)  
        return contrast  
    except Exception as e:  
        print(f"Contrast calculation error: {e}")  
        return 0  

def ChangeColor(url, soup):  
    # Get color information 
    issues = []
    color_info = get_colors(url, soup)  
    
    # Check contrast for each color pair  
    # for info in color_info:  
    #     text_color = info.get('text_color')  
    #     bg_color = info.get('bg_color')  
        
    #     if text_color and bg_color:  
    #         contrast = check_contrast(text_color, bg_color)  
            # print(f"Selector/Element: {info.get('selector', info.get('element', 'Unknown'))}")  
            # print(f"Text Color: {text_color}")  
            # print(f"Background Color: {bg_color}")  
            # print(f"Contrast Ratio: {contrast}")  
            
            # if contrast < 4.5:  
            #     changed_text_color = getColors(text_color, bg_color)
            #     if info['type'] == 1:
            #         info['element']['style'] += f'color: {changed_text_color};'
            #         info['element']['style'] = info['element']['style'].replace(f'color: {text_color};', f'color: {changed_text_color};')
                    
                # issues.append({
                #     info: info,
                #     text_color: changed_text_color, 
                # })

    
    return issues

if "__name__" == "__main__":
    url = "http://192.168.106.164:5000/"
    issues = ChangeColor(url)

    print(issues)