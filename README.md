# Seoul Bike Sharing Demand Prediction

Predicting bike rental demand in Seoul using machine learning, and serving real-time predictions via a Flask web app.

---

## 🚴‍♂️ Project Overview

This project builds a regression model to forecast bike-sharing counts in Seoul based on weather, time, and seasonal features. It includes:

- **Data exploration & preprocessing** in a Jupyter notebook  
- **Model training & evaluation** (several algorithms compared)  
- **Model serialization** for inference  
- **Real-time prediction API** built with Flask  
- **Frontend dashboard** using HTML, CSS, and JavaScript to query the API  

---

## 📁 Repository Structure


├── .git/                       
├── .ipynb_checkpoints/       
│
├── data/                         
│   ├── seoul_bike_sharing.csv  
│   └── processed/  
│       └── features.npy  
│
├── Models/                      
│   ├── random_forest.pkl  
│   └── xgboost.pkl  
│
├── bike_sharing_prediction.ipynb  
│   Exploratory Data Analysis, feature engineering, model training & comparison  
│
├── inference.ipynb             
│
├── src/                          
│   ├── data_loader.py            
│   ├── features.py             
│   ├── model.py                 
│   └── utils.py                  
│
├── api/                          
│   ├── app.py                   
│   └── requirements.txt       
│
├── Dashboard/                    
│   ├── index.html              
│   ├── styles.css            
│   └── script.js                 
│
├── requirements.txt            
├── runtime.txt                 
└── README.md                    
```
🔧 Installation

1. Clone the repo
  
   git clone https://github.com/your-username/seoul-bike-prediction.git
   cd seoul-bike-prediction
   ```

2. **Create & activate a virtual environment**  
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### 1. Training & Evaluation

Open `bike_sharing_prediction.ipynb` to explore the data, engineer features, train several models, and compare their performance.

```bash
jupyter notebook bike_sharing_prediction.ipynb
```

### 2. Batch Inference

Use `inference.ipynb` to load a serialized model and run predictions on new or held-out data.

```bash
jupyter notebook inference.ipynb
```

### 3. Serving Real-Time Predictions

1. **Launch the Flask API**  
   ```bash
   cd api
   python app.py
   ```
2. **Open the Dashboard**  
   In your browser, go to `http://localhost:5000` (or if you have the front-end hosted separately, open `Dashboard/index.html`).  
3. **Enter the required inputs** (e.g. temperature, humidity, season, etc.) and click **“Predict”**. The predicted bike count will appear instantly.

---

## 📊 Dashboard

- Built with vanilla **HTML/CSS/JavaScript**  
- Uses **Fetch API** to POST form data to the Flask endpoint  
- Displays prediction and optional confidence intervals  

---

## ⚙️ Configuration

- **`runtime.txt`**: Specify the Python runtime for platforms like Heroku  
- **`requirements.txt`**: Core packages for data science and model training  
- **`api/requirements.txt`**: Lightweight packages needed to run the Flask service  

---

## 🙏 Acknowledgments

- **Dataset**: [Seoul Bike Sharing Demand Data](https://archive.ics.uci.edu/ml/datasets/Bike+Sharing+Dataset)  
- **Inspiration**: Various Kaggle kernels comparing regression techniques  



## 📄 License

This project is released under the [MIT License](LICENSE).

---

Feel free to star ⭐ the repo if you find it useful, and reach out if you have any questions or suggestions!
