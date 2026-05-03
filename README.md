# PhonePe Transaction Insights

## Project Type
EDA + Machine Learning + Streamlit Dashboard

## Author
Sutirtha Saha

## Project Overview
This project analyzes PhonePe transaction data from 2018 to 2024 
across all Indian states, districts and pin codes to derive 
actionable business insights using SQL, Python and Machine Learning.

## Tech Stack
- Python 3.13
- MySQL
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Scikit-learn

## Project Structure
pulse/
  data/               Raw JSON data from PhonePe Pulse GitHub
  app.py              Streamlit dashboard
  etl.ipynb           Data extraction and loading notebook
  analysis.ipynb      SQL queries and visualization notebook
  ml_model.ipynb      Machine learning models notebook
  README.md           Project documentation

## Database Tables
| Table                  | Rows   |
|------------------------|--------|
| aggregated_transaction | 5454   |
| aggregated_user        | 6919   |
| aggregated_insurance   | 701    |
| map_transaction        | 20604  |
| map_user               | 20608  |
| top_transaction        | 9999   |
| top_user               | 10000  |

## Dashboard Features
- Home Page with KPI cards
- Transaction Analysis with year and quarter filters
- User Analysis with brand and state breakdown
- Insurance Analysis with growth trends
- District Analysis with top performing districts
- Pincode Analysis with micro market insights
- Customer Segmentation using KMeans Clustering
- Fraud Detection using Statistical Analysis
- ML Models with Regression and Classification
- Transaction Forecast for 2025 2026 2027

## ML Models Built
1. Transaction Amount Prediction
   - Linear Regression
   - Random Forest Regressor
   - Metrics: R2 Score, MAE, RMSE

2. Fraud Detection Classification
   - Random Forest Classifier
   - Metrics: Accuracy, AUC Score, Confusion Matrix

3. Transaction Growth Forecast
   - Linear Regression
   - Forecast Years: 2025, 2026, 2027

## How to Run

### Step 1: Clone PhonePe Pulse data
git clone https://github.com/PhonePe/pulse.git

### Step 2: Install all required libraries
pip install mysql-connector-python
pip install pandas numpy
pip install matplotlib seaborn plotly
pip install streamlit
pip install scikit-learn

### Step 3: Setup MySQL Database
- Install MySQL on your laptop
- Open MySQL Workbench
- Create database phonepe_db
- Run etl.ipynb to load all JSON data into MySQL

### Step 4: Run the Streamlit Dashboard
streamlit run app.py

### Step 5: Open in browser
http://localhost:8501

## Key Insights
1. Maharashtra leads all states in total transaction volume
2. Peer to Peer payments dominate with over 50% share
3. Q4 festive season consistently drives highest volumes
4. COVID-19 in 2020 was the biggest catalyst for growth
5. Xiaomi and Samsung dominate the PhonePe user device base
6. Insurance transactions growing faster than overall transactions
7. High value states contribute nearly 60% of total volume
8. Several states show high registrations but low app engagement
9. Budget Android phones are the primary payment devices
10. Metro city pincodes drive disproportionately high volumes

## Business Recommendations
1. Expand merchant payment network in tier 2 and tier 3 cities
2. Re-engage dormant users through personalized campaigns
3. Optimize app performance for budget Android devices
4. Scale insurance products to meet growing post COVID demand
5. Plan major campaigns around Q4 festive season every year
6. Target underserved northeastern states with digital literacy programs
7. Deploy hyperlocal campaigns in top performing metro pincodes
8. Implement real time fraud detection system in production
9. Add two factor authentication for high value transactions
10. Cross sell insurance products to active transaction users

## Customer Segments
- High Value States: Maharashtra, Karnataka, Telangana
- Medium Value States: Rajasthan, UP, Tamil Nadu, Gujarat
- Low Value States: Northeastern states and small UTs

## Fraud Detection
- Method: Statistical Anomaly Detection
- Threshold: 3 Standard Deviations above mean
- Model: Random Forest Classifier
- Key Signal: Average Transaction Value

## Project Deliverables
1. etl.ipynb        - Data extraction and MySQL loading
2. analysis.ipynb   - SQL queries and visualizations  
3. ml_model.ipynb   - Machine learning models
4. app.py           - Interactive Streamlit dashboard
5. README.md        - Complete project documentation

## Dataset Source
GitHub: https://github.com/PhonePe/pulse

## Connect with Me
GitHub: https://github.com/Sutirtha08-dotcom