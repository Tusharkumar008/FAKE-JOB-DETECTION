# FAKE-JOB-DETECTION

# Fake Job Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Flask-green)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange)

## 📌 Project Overview
The **Fake Job Detection** project is a Machine Learning application designed to identify fraudulent job postings. By analyzing various features of a job advertisement—such as the company profile, job description, and requirements—the model classifies the posting as either **Real** or **Fake**.

This tool helps job seekers and platforms filter out scams, ensuring a safer job search experience.

## 📂 Dataset
This project typically utilizes the [Real or Fake Job Posting Prediction dataset](https://www.kaggle.com/shivamb/real-or-fake-fake-jobposting-prediction) from Kaggle, which contains ~18,000 job descriptions with binary classification labels.

## 🛠️ Tech Stack
* **Programming Language**: Python
* **Web Framework**: Flask
* **Machine Learning**: Scikit-Learn, Pandas, NumPy, NLTK (Natural Language Toolkit)
* **Frontend**: HTML, CSS

## ⚙️ Installation

Follow these steps to set up the project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Tusharkumar008/FAKE-JOB-DETECTION.git](https://github.com/Tusharkumar008/FAKE-JOB-DETECTION.git)
    cd FAKE-JOB-DETECTION
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    Ensure you have `pip` installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage / Hosting

To host the website and run the application locally, use the following command:

```bash
python app.py
