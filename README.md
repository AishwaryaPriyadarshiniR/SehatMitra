**SehatMitra — AI-Powered Healthcare Chatbot**

SehatMitra is an intelligent, data-driven healthcare assistant designed to help users assess health concerns through a conversational chatbot interface. The system combines machine learning, natural language processing, and medical datasets to provide preliminary triage guidance and home-care recommendations in a user-friendly manner.

---

## 🎯 **Project Objective**

The goal of SehatMitra is to assist common users in:

* Understanding the urgency of their symptoms
* Identifying a likely medical condition based on symptom patterns
* Receiving safe, data-backed home-care precautions
* Getting guidance on whether to seek medical attention

SehatMitra is **not a diagnostic tool**, but a decision-support assistant that helps users make informed health-related decisions.

---

## 🏗 **System Architecture**

The system follows a hybrid AI architecture combining machine learning, rule-based logic, and an LLM-based conversational layer:

1. **User Input (Frontend)**

   * Chat-based web interface built with HTML, CSS, and JavaScript
   * Accepts symptoms in natural language

2. **Symptom Normalization (NLP Layer)**

   * Converts user-friendly symptom descriptions into structured, dataset-compatible terms
   * Bridges the gap between real-world language and training data

3. **Triage Classification (ML Model)**

   * Predicts urgency level:

     * 🏠 Home Care
     * 🩺 Doctor Soon
     * 🚨 Emergency
   * Trained using TF-IDF vectorization + Logistic Regression

4. **Disease Prediction (ML Model)**

   * Predicts the most likely condition based on symptom patterns
   * Trained on a Kaggle disease–symptom dataset using TF-IDF + Logistic Regression

5. **Knowledge Retrieval (Medical Datasets)**

   * Fetches:

     * Disease descriptions (`symptom_Description.csv`)
     * Home-care precautions (`symptom_precaution.csv`)

6. **Conversational Polishing (LLM Layer)**

   * Uses **Mistral AI (via Hugging Face Inference API)** to refine and structure responses in a friendly tone
   * Operates only as a presentation layer — medical decisions come from ML models and rules

7. **Safety & Rule-Based Overrides**

   * Handles common cases such as:

     * Common cold
     * Acute diarrhea
     * Prolonged fever
   * Prevents incorrect predictions when data is insufficient

---

## 🛠 **Tech Stack**

### **Frontend**

* HTML, CSS, JavaScript
* Chat-style UI with message bubbles and typing indicator

### **Backend**

* Flask (Python web framework)

### **Machine Learning**

* Python
* scikit-learn

  * TF-IDF Vectorizer
  * Logistic Regression

### **NLP & Preprocessing**

* Custom Symptom Normalization Module

### **Datasets (Kaggle)**

* `dataset.csv` → Disease–Symptom mapping (model training)
* `symptom_precaution.csv` → Home remedies / precautions
* `symptom_Description.csv` → Disease explanations
* `text_triage_dataset.csv` → Derived dataset for urgency classification

### **LLM Layer**

* Mistral AI (`Mistral-7B-Instruct-v0.2`) via Hugging Face (optional response polishing)

### **Model Storage**

* `joblib` for saving and loading trained ML models (`.pkl` files)

---

## 🚀 **Features**

* Conversational chatbot interface
* ML-based urgency classification
* Data-trained disease prediction
* Dataset-backed home-care guidance
* Symptom normalization for real-world text
* Hybrid ML + rule-based decision system
* Optional multilingual and voice support (future work)

---

## ⚠️ **Disclaimer**

SehatMitra is intended for **informational and preliminary guidance only**. It does **not** replace professional medical diagnosis or treatment. Users are encouraged to consult qualified healthcare professionals for serious or persistent symptoms.

---

## 📌 **Future Enhancements**

* Multilingual support (Hindi + English)
* Voice input and output
* Confidence scores for predictions
* Interactive follow-up questions
* Improved medical safety guardrails

---

## 👩‍💻 **Developed By**

Aishwarya Priyadarshini R
SehatMitra Project
