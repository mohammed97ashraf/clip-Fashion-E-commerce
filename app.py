from flask import Flask, render_template,request, jsonify
from utils.create_vector_db import create_embadding, search_with_text


app = Flask(__name__)


# Define the directory to store temporary uploaded images
UPLOAD_FOLDER = 'temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/text_search', methods=['POST'])
def text_search():
    search_text = request.json.get('text', '').lower()
    # Filter products based on search text
    #filtered_products = [product for product in products if search_text in product['name'].lower()]
    product_list = search_with_text(search_text)
    filtered_products = [{"name":products.payload['productDisplayName'],"image":products.payload["base_64_image"]} for products in product_list]
    return jsonify(filtered_products)

@app.route('/image_search', methods=['POST'])
def image_search():
    # Check if a file was uploaded
    if 'file' not in request.files:
        print("image not fount")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Save the uploaded image to the temporary folder
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform image search and get results
        #results = perform_image_search(filepath)

        # Delete the uploaded image after processing
        os.remove(filepath)

        # Return the search results
        return jsonify(products)
    
    
if __name__ == "__main__":
    create_embadding()
    app.run(debug=True)