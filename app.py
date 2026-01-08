from flask import Flask, render_template, request, jsonify
import joblib
import re
import numpy as np
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

# Load the trained model
try:
    model = joblib.load('fake_job_model.pkl')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def clean_text(text):
    """Clean and preprocess text"""
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = text.lower()
    text = ' '.join(text.split())
    return text

def explain_prediction(text, pipeline):
    """Explain the prediction by finding important words"""
    # Get the vectorizer and classifier from the pipeline
    vectorizer = pipeline.named_steps['tfidf']
    clf = pipeline.named_steps['clf']
    
    # Get word importance (coefficients)
    feature_names = vectorizer.get_feature_names_out()
    coefs = clf.coef_.flatten()
    word_map = dict(zip(feature_names, coefs))
    
    # Check words in the specific text input
    words = set(re.findall(r'\b\w+\b', text.lower()))
    
    # Separate into "Red Flags" (Fake indicators) and "Green Flags" (Real)
    red_flags = []
    green_flags = []
    
    for word in words:
        if word in word_map:
            score = word_map[word]
            # If score is high positive -> Fake
            if score > 0.5: 
                red_flags.append((word, round(float(score), 3)))
            # If score is high negative -> Real
            elif score < -0.5:
                green_flags.append((word, round(float(score), 3)))
                
    return sorted(red_flags, key=lambda x: x[1], reverse=True), sorted(green_flags, key=lambda x: x[1])

def create_wordcloud(text):
    """Create word cloud image and return as base64 string"""
    if not text or len(text.strip()) < 10:
        return None
    
    plt.figure(figsize=(10, 6))
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        colormap='viridis',
        max_words=100
    ).generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    plt.close()
    
    # Encode to base64
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return image_base64

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please train the model first.'
        }), 500
    
    # Get data from request
    data = request.json
    job_description = data.get('job_description', '')
    
    if not job_description:
        return jsonify({
            'error': 'Please enter a job description.'
        }), 400
    
    # Clean and preprocess the text
    cleaned_text = clean_text(job_description)
    
    # Make prediction
    try:
        prediction = model.predict([cleaned_text])[0]
        probabilities = model.predict_proba([cleaned_text])[0]
        
        # Get explanation
        red_flags, green_flags = explain_prediction(cleaned_text, model)
        
        # Create word cloud
        wordcloud_img = create_wordcloud(job_description)
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'probabilities': {
                'real': round(float(probabilities[0]) * 100, 2),
                'fake': round(float(probabilities[1]) * 100, 2)
            },
            'red_flags': red_flags[:10],  # Top 10 red flags
            'green_flags': green_flags[:10],  # Top 10 green flags
            'wordcloud': wordcloud_img
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

@app.route('/analysis')
def analysis():
    """Show training data analysis"""
    return render_template('analysis.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)