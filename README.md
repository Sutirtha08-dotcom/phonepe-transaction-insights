# PhonePe Transaction Insights

## Project Overview
This project analyzes PhonePe transaction data from 2018 to 2024
to derive business insights about digital payment trends in India.

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
  data/              Raw JSON data from PhonePe Pulse GitHub
  app.py             Streamlit dashboard
  etl.ipynb          Data extraction and loading notebook
  analysis.ipynb     SQL queries and visualization notebook
  README.md          Project documentation

## How to Run

### Step 1: Clone the data
git clone https://github.com/PhonePe/pulse.git

### Step 2: Install required libraries
pip install mysql-connector-python pandas matplotlib
pip install seaborn plotly streamlit scikit-learn

### Step 3: Set up MySQL
- Install MySQL
- Create database phonepe_db
- Run etl.ipynb to load all data

### Step 4: Run Streamlit dashboard
streamlit run app.py

## Database Tables
- aggregated_transaction : 5454 rows
- aggregated_user        : 6919 rows
- aggregated_insurance   : 701 rows
- map_transaction        : 20604 rows
- map_user               : 20608 rows
- top_transaction        : 9999 rows
- top_user               : 10000 rows

## Dashboard Features
- Home Page with KPI cards
- Transaction Analysis with filters
- User Analysis
- Insurance Analysis
- District Analysis
- Pincode Analysis
- Customer Segmentation using KMeans
- Fraud Detection using Statistical Analysis

## Key Insights
1. Maharashtra leads all states in total transaction volume
2. Peer to Peer payments dominate with over 50% share
3. Q4 consistently shows highest transaction volumes
4. User growth accelerated sharply post COVID-19 in 2020
5. Insurance transactions growing rapidly after 2020
6. Xiaomi and Samsung dominate the PhonePe user device base
7. Top districts are state capitals and commercial hubs
8. High value states contribute 60% of total transaction value
9. Several states show high registrations but low app engagement
10. Festive season Q4 shows disproportionately high volumes

## Business Recommendations
1. Expand merchant payment network in tier 2 and tier 3 cities
2. Re-engage dormant users through personalized campaigns
3. Optimize app for budget Android devices especially Xiaomi
4. Scale insurance products to meet growing post COVID demand
5. Plan major campaigns around Q4 festive season every year
6. Target underserved states with digital literacy programs
7. Deploy hyperlocal campaigns in top performing pincodes
8. Implement real time fraud detection system
9. Add two factor authentication for high value transactions
10. Cross sell insurance to active transaction users

## Project Deliverables
1. etl.ipynb        Data extraction and MySQL loading code
2. analysis.ipynb   SQL queries and visualizations
3. app.py           Interactive Streamlit dashboard
4. README.md        Project documentation

## Author
Sutirtha Saha

## Dataset Source
GitHub: https://github.com/PhonePe/pulse