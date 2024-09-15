import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Path to the JSON file
FAQS_FILE = 'data/faqs.json'

# Helper function to read FAQs from the JSON file
def load_faqs():
    with open(FAQS_FILE, 'r') as f:
        return json.load(f)

# Helper function to save FAQs to the JSON file
def save_faqs(faqs):
    with open(FAQS_FILE, 'w') as f:
        json.dump(faqs, f, indent=4)

# GET all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    faqs = load_faqs()
    return jsonify(faqs), 200

# GET a single FAQ by ID
@app.route('/faqs/<int:id>', methods=['GET'])
def get_faq(id):
    faqs = load_faqs()
    faq = next((faq for faq in faqs if faq['id'] == id), None)
    if faq:
        return jsonify(faq), 200
    return jsonify({'error': 'FAQ not found'}), 404

# POST a new FAQ
@app.route('/faqs', methods=['POST'])
def create_faq():
    faqs = load_faqs()
    new_faq = request.get_json()
    new_faq['id'] = max(faq['id'] for faq in faqs) + 1 if faqs else 1
    faqs.append(new_faq)
    save_faqs(faqs)
    return jsonify(new_faq), 201

# PUT to update an FAQ by ID
@app.route('/faqs/<int:id>', methods=['PUT'])
def update_faq(id):
    faqs = load_faqs()
    faq = next((faq for faq in faqs if faq['id'] == id), None)
    if faq:
        data = request.get_json()
        faq.update(data)
        save_faqs(faqs)
        return jsonify(faq), 200
    return jsonify({'error': 'FAQ not found'}), 404

# DELETE an FAQ by ID
@app.route('/faqs/<int:id>', methods=['DELETE'])
def delete_faq(id):
    faqs = load_faqs()
    faq = next((faq for faq in faqs if faq['id'] == id), None)
    if faq:
        faqs.remove(faq)
        save_faqs(faqs)
        return jsonify({'message': 'FAQ deleted'}), 200
    return jsonify({'error': 'FAQ not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
