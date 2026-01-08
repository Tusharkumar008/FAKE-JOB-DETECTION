import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('fake_real_job_postings.csv')

# Handle missing values in text columns
df['job_description'] = df['job_description'].fillna('')
df['requirements'] = df['requirements'].fillna('')
df['benefits'] = df['benefits'].fillna('')

# Combine text features for better prediction
df['combined_text'] = df['job_description'] + ' ' + df['requirements'] + ' ' + df['benefits']

# Clean text
def clean_text(text):
    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

df['combined_text'] = df['combined_text'].apply(clean_text)

# Prepare data
X = df['combined_text']
y = df['is_fake']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create and train the pipeline
print("Training model...")
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2)
    )),
    ('clf', LogisticRegression(
        random_state=42,
        max_iter=1000,
        class_weight='balanced'
    ))
])

# Train the model
pipeline.fit(X_train, y_train)

# Save the model
joblib.dump(pipeline, 'fake_job_model.pkl')
print("Model saved as 'fake_job_model.pkl'")

# Calculate and display model performance
train_score = pipeline.score(X_train, y_train)
test_score = pipeline.score(X_test, y_test)
print(f"Training Accuracy: {train_score:.2%}")
print(f"Testing Accuracy: {test_score:.2%}")

# Create visualizations
print("Creating visualizations...")

# 1. Distribution of real vs fake jobs
plt.figure(figsize=(10, 6))
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Pie chart
real_count = (y == 0).sum()
fake_count = (y == 1).sum()
ax1.pie([real_count, fake_count], 
        labels=['Real Jobs', 'Fake Jobs'],
        autopct='%1.1f%%',
        colors=['#2ecc71', '#e74c3c'])
ax1.set_title('Distribution of Real vs Fake Jobs')

# Bar chart
ax2.bar(['Real Jobs', 'Fake Jobs'], [real_count, fake_count], 
        color=['#2ecc71', '#e74c3c'])
ax2.set_ylabel('Count')
ax2.set_title('Number of Real vs Fake Jobs')
ax2.text(0, real_count + 5, str(real_count), ha='center')
ax2.text(1, fake_count + 5, str(fake_count), ha='center')

plt.tight_layout()
plt.savefig('static/training_distribution.png', dpi=100, bbox_inches='tight')
plt.close()

# 2. Word clouds for real and fake jobs
fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(16, 8))

# Real jobs word cloud
real_text = ' '.join(df[df['is_fake'] == 0]['combined_text'])
wordcloud_real = WordCloud(
    width=800, 
    height=400, 
    background_color='white',
    colormap='viridis',
    max_words=100
).generate(real_text)
ax3.imshow(wordcloud_real, interpolation='bilinear')
ax3.set_title('Common Words in Real Job Postings')
ax3.axis('off')

# Fake jobs word cloud
fake_text = ' '.join(df[df['is_fake'] == 1]['combined_text'])
wordcloud_fake = WordCloud(
    width=800, 
    height=400, 
    background_color='white',
    colormap='Reds',
    max_words=100
).generate(fake_text)
ax4.imshow(wordcloud_fake, interpolation='bilinear')
ax4.set_title('Common Words in Fake Job Postings')
ax4.axis('off')

plt.tight_layout()
plt.savefig('static/wordclouds.png', dpi=100, bbox_inches='tight')
plt.close()

# 3. Top industries for real and fake jobs
fig3, (ax5, ax6) = plt.subplots(1, 2, figsize=(16, 8))

# Real jobs by industry
real_industries = df[df['is_fake'] == 0]['industry'].value_counts().head(10)
ax5.barh(range(len(real_industries)), real_industries.values, color='#2ecc71')
ax5.set_yticks(range(len(real_industries)))
ax5.set_yticklabels(real_industries.index)
ax5.invert_yaxis()
ax5.set_xlabel('Count')
ax5.set_title('Top Industries for Real Jobs')

# Fake jobs by industry
fake_industries = df[df['is_fake'] == 1]['industry'].value_counts().head(10)
ax6.barh(range(len(fake_industries)), fake_industries.values, color='#e74c3c')
ax6.set_yticks(range(len(fake_industries)))
ax6.set_yticklabels(fake_industries.index)
ax6.invert_yaxis()
ax6.set_xlabel('Count')
ax6.set_title('Top Industries for Fake Jobs')

plt.tight_layout()
plt.savefig('static/industry_distribution.png', dpi=100, bbox_inches='tight')
plt.close()

print("Visualizations saved in 'static/' folder")
print("Model training complete!")