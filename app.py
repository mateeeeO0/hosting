from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image
import io
import requests

app = Flask(__name__)
CORS(app) 

def apply_grayscale(image):
    return image.convert("L").convert("RGB")

def apply_sepia(image):
    sepia = Image.new("RGB", image.size)
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            sepia.putpixel((x, y), (min(tr, 255), min(tg, 255), min(tb, 255)))
    return sepia

def apply_vintage(image):
    vintage = Image.new("RGB", image.size)
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            r = min(int(r * 0.8 + 20), 255)
            g = min(int(g * 0.7 + 15), 255)
            b = min(int(b * 0.5 + 10), 255)
            vintage.putpixel((x, y), (r, g, b))
    return vintage

@app.route('/upload', methods=['POST'])
def upload():
    image_url = request.form.get('image_url')
    filter_type = request.form.get('filter')
    
    if not image_url or not filter_type:
        return 'Parámetros incompletos', 400
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except Exception as e:
        return f'Error al descargar la imagen: {e}', 400

    image = Image.open(io.BytesIO(response.content)).convert('RGB')

    if filter_type == 'grayscale':
        processed = apply_grayscale(image)
    elif filter_type == 'sepia':
        processed = apply_sepia(image)
    elif filter_type == 'vintage':
        processed = apply_vintage(image)
    else:
        return 'Filtro no válido', 400

    buffer = io.BytesIO()
    processed.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

@app.route('/')
def home():
    return "Servidor activo"


