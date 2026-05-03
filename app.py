import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="PhonePe Transaction Insights",
    page_icon="📱",
    layout="wide"
)

@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="08S12t1995@",
        database="phonepe_db"
    )

conn = get_connection()

def run_query(query):
    return pd.read_sql(query, conn)

st.sidebar.title("📱 PhonePe Insights")
st.sidebar.markdown("---")

menu = st.sidebar.selectbox("Select Analysis", [
    "Home",
    "Transaction Analysis",
    "User Analysis",
    "Insurance Analysis",
    "District Analysis",
    "Pincode Analysis",
    "Customer Segmentation",
    "Fraud Detection",
    "ML Models",
    "Transaction Forecast"
])

if menu == "Home":
    st.title("📱 PhonePe Transaction Insights Dashboard")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    total_amount = run_query("""
        SELECT SUM(transaction_amount) AS total
        FROM aggregated_transaction
        WHERE state='india'
    """)

    total_count = run_query("""
        SELECT SUM(transaction_count) AS total
        FROM aggregated_transaction
        WHERE state='india'
    """)

    total_users = run_query("""
        SELECT SUM(registered_users) AS total
        FROM map_user
    """)

    total_insurance = run_query("""
        SELECT SUM(insurance_amount) AS total
        FROM aggregated_insurance
        WHERE state='india'
    """)

    with col1:
        st.metric(
            "💰 Total Transaction Amount",
            f"₹{total_amount['total'][0]/1e12:.2f} Trillion"
        )
    with col2:
        st.metric(
            "🔢 Total Transactions",
            f"{total_count['total'][0]/1e9:.2f} Billion"
        )
    with col3:
        st.metric(
            "👥 Total Registered Users",
            f"{total_users['total'][0]/1e6:.2f} Million"
        )
    with col4:
        st.metric(
            "🛡️ Total Insurance Amount",
            f"₹{total_insurance['total'][0]/1e9:.2f} Billion"
        )

    st.markdown("---")
    st.subheader("📈 Yearly Transaction Growth")

    df_yearly = run_query("""
        SELECT year,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count) AS total_count
        FROM aggregated_transaction
        WHERE state = 'india'
        GROUP BY year
        ORDER BY year
    """)

    fig = px.line(
        df_yearly,
        x='year',
        y='total_amount',
        markers=True,
        title='Yearly Transaction Growth',
        color_discrete_sequence=['#5F2D91']
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Overall Key Insights")
    st.markdown("""
    - PhonePe has grown exponentially from 2018 to 2024
    - Maharashtra leads all states in total transaction volume
    - COVID-19 was the biggest catalyst for digital payment adoption in 2020
    - Q4 is consistently the highest performing quarter every year
    - Budget Android phones drive the majority of PhonePe user base
    - Insurance transactions are growing faster than overall transactions
    """)

    st.markdown("---")
    st.subheader("✅ Overall Business Recommendations")
    st.markdown("""
    - Expand merchant payment network in tier 2 and tier 3 cities
    - Re-engage dormant users through personalized campaigns
    - Optimize app for low end Android devices especially Xiaomi
    - Scale insurance products to meet growing post COVID demand
    - Plan major campaigns around Q4 festive season every year
    - Target underserved states with digital literacy programs
    """)

elif menu == "Transaction Analysis":
    st.title("💰 Transaction Analysis")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox(
            "Select Year",
            options=[2018, 2019, 2020, 2021, 2022, 2023, 2024]
        )
    with col2:
        quarter = st.selectbox(
            "Select Quarter",
            options=[1, 2, 3, 4]
        )

    st.markdown("---")
    st.subheader("🏆 Top 10 States by Transaction Amount")

    df_states = run_query(f"""
        SELECT state,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count) AS total_count
        FROM aggregated_transaction
        WHERE state != 'india'
        AND year = {year}
        AND quarter = {quarter}
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_states,
        x='state',
        y='total_amount',
        color='total_amount',
        color_continuous_scale='Purples',
        title=f'Top 10 States - {year} Q{quarter}'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🥧 Transaction Type Distribution")

    df_types = run_query(f"""
        SELECT transaction_type,
               SUM(transaction_amount) AS total_amount
        FROM aggregated_transaction
        WHERE state = 'india'
        AND year = {year}
        AND quarter = {quarter}
        GROUP BY transaction_type
    """)

    fig = px.pie(
        df_types,
        names='transaction_type',
        values='total_amount',
        title='Transaction Type Distribution',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Transaction Heatmap by Year and Quarter")

    df_heat = run_query("""
        SELECT year, quarter,
               SUM(transaction_amount) AS total_amount
        FROM aggregated_transaction
        WHERE state = 'india'
        GROUP BY year, quarter
        ORDER BY year, quarter
    """)

    df_pivot = df_heat.pivot(
        index='year',
        columns='quarter',
        values='total_amount'
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        df_pivot,
        annot=True,
        fmt='.2e',
        cmap='Purples',
        linewidths=0.5,
        ax=ax
    )
    ax.set_title('Transaction Heatmap')
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - Maharashtra, Karnataka and Telangana contribute nearly 40% of total transactions
    - Peer to Peer payments dominate with over 50% of total volume
    - Q4 consistently shows highest transaction volumes due to festive season
    - Transaction amounts grew exponentially after 2020 due to COVID-19
    - Bottom 10 states show very low digital payment adoption
    - Average transaction amount is highest in commercial hub states
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Focus on growing merchant payments in tier 2 and tier 3 cities
    - Plan special cashback campaigns every Q4 for festive season
    - Invest in digital infrastructure in low performing states
    - Target high average transaction states with premium business products
    - Run awareness campaigns in bottom 10 states to improve adoption
    """)

elif menu == "User Analysis":
    st.title("👥 User Analysis")
    st.markdown("---")

    st.subheader("📱 Top 10 Mobile Brands")

    df_brands = run_query("""
        SELECT brand,
               SUM(user_count) AS total_users
        FROM aggregated_user
        WHERE state = 'india'
        GROUP BY brand
        ORDER BY total_users DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_brands,
        x='brand',
        y='total_users',
        color='total_users',
        color_continuous_scale='Purples',
        title='Top 10 Mobile Brands by User Count'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 User Growth by Year")

    df_user_growth = run_query("""
        SELECT year,
               SUM(user_count) AS total_users
        FROM aggregated_user
        WHERE state = 'india'
        GROUP BY year
        ORDER BY year
    """)

    fig = px.line(
        df_user_growth,
        x='year',
        y='total_users',
        markers=True,
        color_discrete_sequence=['#5F2D91'],
        title='User Growth by Year'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Top 10 States: Registered Users vs App Opens")

    df_users = run_query("""
        SELECT state,
               SUM(registered_users) AS total_users,
               SUM(app_opens) AS total_app_opens
        FROM map_user
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_users,
        x='state',
        y=['total_users', 'total_app_opens'],
        barmode='group',
        title='Registered Users vs App Opens by State'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - Xiaomi and Samsung together account for nearly 50% of all PhonePe users
    - User registrations grew sharply after 2020 due to COVID-19 pandemic
    - Several states show high registrations but significantly low app open rates
    - Uttar Pradesh has high user count but lower engagement than Maharashtra
    - Apple users are few in number but represent high value customers
    - Young users on Realme devices represent a fast growing segment
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Optimize app performance for Xiaomi and Samsung budget devices
    - Run re-engagement campaigns in states with low app open rates
    - Introduce referral programs to convert dormant users into active users
    - Develop premium features for Apple users to increase transaction value
    - Target young Realme users with student offers and gaming payment features
    """)

elif menu == "Insurance Analysis":
    st.title("🛡️ Insurance Analysis")
    st.markdown("---")

    st.subheader("📈 Insurance Growth by Year")

    df_insurance = run_query("""
        SELECT year,
               SUM(insurance_amount) AS total_amount,
               SUM(insurance_count) AS total_count
        FROM aggregated_insurance
        WHERE state = 'india'
        GROUP BY year
        ORDER BY year
    """)

    fig = px.line(
        df_insurance,
        x='year',
        y='total_amount',
        markers=True,
        color_discrete_sequence=['green'],
        title='Insurance Amount Growth by Year'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🥧 Insurance Type Distribution")

    df_ins_type = run_query("""
        SELECT insurance_type,
               SUM(insurance_amount) AS total_amount,
               SUM(insurance_count) AS total_count
        FROM aggregated_insurance
        WHERE state = 'india'
        GROUP BY insurance_type
    """)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            df_ins_type,
            names='insurance_type',
            values='total_amount',
            title='Insurance By Amount'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(
            df_ins_type,
            names='insurance_type',
            values='total_count',
            title='Insurance By Count'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top 10 States by Insurance Amount")

    df_ins_states = run_query("""
        SELECT state,
               SUM(insurance_amount) AS total_amount
        FROM aggregated_insurance
        WHERE state != 'india'
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_ins_states,
        x='state',
        y='total_amount',
        color='total_amount',
        color_continuous_scale='Greens',
        title='Top 10 States by Insurance Amount'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - Insurance transactions grew dramatically after 2020 due to COVID awareness
    - Only one or two insurance types dominate total insurance volume
    - States leading in transactions also lead in insurance purchases
    - Users prefer simple and affordable insurance products on digital platforms
    - Insurance is growing faster proportionally than overall transactions
    - Several high transaction states show untapped insurance potential
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Introduce more affordable and simple insurance products
    - Target digitally active states for insurance cross selling campaigns
    - Educate users in low performing states about digital insurance benefits
    - Cross sell insurance to existing active transaction users
    - Partner with insurance companies to offer exclusive PhonePe insurance deals
    """)

elif menu == "District Analysis":
    st.title("🏙️ District Analysis")
    st.markdown("---")

    st.subheader("🏆 Top 10 Districts by Transaction Amount")

    df_districts = run_query("""
        SELECT district,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count) AS total_count
        FROM map_transaction
        GROUP BY district
        ORDER BY total_amount DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_districts,
        x='district',
        y='total_amount',
        color='total_amount',
        color_continuous_scale='Oranges',
        title='Top 10 Districts by Transaction Amount'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("👥 Top 10 Districts by Registered Users")

    df_dist_users = run_query("""
        SELECT district,
               SUM(registered_users) AS total_users
        FROM map_user
        GROUP BY district
        ORDER BY total_users DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_dist_users,
        x='district',
        y='total_users',
        color='total_users',
        color_continuous_scale='Blues',
        title='Top 10 Districts by Registered Users'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - State capitals and commercial hubs dominate district level transactions
    - Bangalore Urban, Mumbai and Hyderabad consistently appear in top 10
    - High transaction districts also show high registered user counts
    - Commercial activity is the primary driver of digital payment adoption
    - Some districts show high users but lower transactions indicating untapped potential
    - District level data reveals micro market opportunities for targeted campaigns
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Deploy dedicated merchant support teams in top performing districts
    - Focus merchant onboarding in districts with high users but low transactions
    - Partner with local businesses in top districts for exclusive payment offers
    - Run district level awareness campaigns in low performing areas
    - Use district data to assign sales territories for merchant acquisition teams
    """)

elif menu == "Pincode Analysis":
    st.title("📍 Pincode Analysis")
    st.markdown("---")

    st.subheader("🏆 Top 10 Pincodes by Transaction Amount")

    df_pincodes = run_query("""
        SELECT pincode,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count) AS total_count
        FROM top_transaction
        GROUP BY pincode
        ORDER BY total_amount DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_pincodes,
        x='pincode',
        y='total_amount',
        color='total_amount',
        color_continuous_scale='Reds',
        title='Top 10 Pincodes by Transaction Amount'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("👥 Top 10 Pincodes by Registered Users")

    df_pin_users = run_query("""
        SELECT pincode,
               SUM(registered_users) AS total_users
        FROM top_user
        GROUP BY pincode
        ORDER BY total_users DESC
        LIMIT 10
    """)

    fig = px.bar(
        df_pin_users,
        x='pincode',
        y='total_users',
        color='total_users',
        color_continuous_scale='Greens',
        title='Top 10 Pincodes by Registered Users'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Insights")
    st.markdown("""
    - Certain metro city pincodes show extremely high transaction volumes
    - Top pincodes are central business districts and commercial zones
    - High transaction pincodes also show high registered user counts
    - Pincode level data helps identify micro markets for targeted campaigns
    - Metro pincodes drive disproportionately high transaction values
    - Some pincodes show high users but lower transactions indicating growth potential
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Deploy business payment solutions in top transaction pincodes
    - Offer exclusive merchant deals in high volume commercial pincodes
    - Use pincode data to plan hyperlocal marketing campaigns
    - Assign dedicated merchant executives to top 10 pincodes
    - Run pincode specific cashback offers to boost transaction volumes
    """)

elif menu == "Customer Segmentation":
    st.title("👥 Customer Segmentation")
    st.markdown("---")

    # Install sklearn if needed
    try:
        from sklearn.preprocessing import StandardScaler
        from sklearn.cluster import KMeans
    except:
        st.error("Please run: pip install scikit-learn")
        st.stop()

    # Fetch data
    df_seg = run_query("""
        SELECT
            state,
            SUM(transaction_amount) AS total_amount,
            SUM(transaction_count) AS total_count,
            AVG(transaction_amount) AS avg_amount,
            SUM(transaction_amount) / SUM(transaction_count) AS avg_txn_value
        FROM aggregated_transaction
        WHERE state != 'india'
        GROUP BY state
    """)

    # Scale data
    features = ['total_amount', 'total_count', 'avg_amount', 'avg_txn_value']
    X = df_seg[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # KMeans clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_seg['cluster'] = kmeans.fit_predict(X_scaled)

    # Sort clusters by total amount
    cluster_means = df_seg.groupby('cluster')['total_amount'].mean().sort_values(ascending=False)
    rank_map = {cluster: rank for rank, cluster in enumerate(cluster_means.index)}
    df_seg['cluster_rank'] = df_seg['cluster'].map(rank_map)

    segment_labels = {
        0: '🥇 High Value States',
        1: '🥈 Medium Value States',
        2: '🥉 Low Value States'
    }
    df_seg['segment'] = df_seg['cluster_rank'].map(segment_labels)

    # ── KPI Cards ─────────────────────────────────────────
    st.subheader("📊 Segment Overview")
    col1, col2, col3 = st.columns(3)

    high = df_seg[df_seg['segment'] == '🥇 High Value States']
    med = df_seg[df_seg['segment'] == '🥈 Medium Value States']
    low = df_seg[df_seg['segment'] == '🥉 Low Value States']

    with col1:
        st.metric("🥇 High Value States", f"{len(high)} States")
    with col2:
        st.metric("🥈 Medium Value States", f"{len(med)} States")
    with col3:
        st.metric("🥉 Low Value States", f"{len(low)} States")

    st.markdown("---")

    # ── Elbow Chart ───────────────────────────────────────
    st.subheader("📈 Elbow Method - Finding Optimal Clusters")
    inertia = []
    K_range = range(2, 10)
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertia.append(km.inertia_)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(list(K_range), inertia, marker='o',
            color='purple', linewidth=2)
    ax.set_title('Elbow Method - Optimal K')
    ax.set_xlabel('Number of Clusters (K)')
    ax.set_ylabel('Inertia')
    st.pyplot(fig)

    st.markdown("---")

    # ── Cluster Scatter Plot ──────────────────────────────
    st.subheader("🗺️ State Segmentation Map")
    fig = px.scatter(
        df_seg,
        x='total_count',
        y='total_amount',
        color='segment',
        text='state',
        title='Customer Segmentation by State',
        color_discrete_map={
            '🥇 High Value States': 'green',
            '🥈 Medium Value States': 'blue',
            '🥉 Low Value States': 'red'
        },
        size='total_amount',
        size_max=50
    )
    fig.update_traces(textposition='top center', textfont_size=9)
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Segment Bar Chart ─────────────────────────────────
    st.subheader("💰 Average Transaction Amount by Segment")
    seg_summary = df_seg.groupby('segment').agg(
        num_states=('state', 'count'),
        avg_total_amount=('total_amount', 'mean'),
        avg_txn_value=('avg_txn_value', 'mean')
    ).reset_index()

    fig = px.bar(
        seg_summary,
        x='segment',
        y='avg_total_amount',
        color='segment',
        title='Average Transaction Amount by Segment',
        color_discrete_map={
            '🥇 High Value States': 'green',
            '🥈 Medium Value States': 'blue',
            '🥉 Low Value States': 'red'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── State List per Segment ────────────────────────────
    st.subheader("📋 States in Each Segment")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🥇 High Value")
        for state in high['state'].tolist():
            st.markdown(f"- {state}")

    with col2:
        st.markdown("### 🥈 Medium Value")
        for state in med['state'].tolist():
            st.markdown(f"- {state}")

    with col3:
        st.markdown("### 🥉 Low Value")
        for state in low['state'].tolist():
            st.markdown(f"- {state}")

    st.markdown("---")

    # ── Insights ──────────────────────────────────────────
    st.subheader("💡 Segmentation Insights")

    st.markdown("#### 🥇 High Value States")
    st.markdown("""
    - Maharashtra, Karnataka and Telangana lead all other states
    - These states contribute nearly 60% of total transaction value
    - High urban population and strong business ecosystems drive volumes
    - Average transaction value is significantly higher than other segments
    """)

    st.markdown("#### 🥈 Medium Value States")
    st.markdown("""
    - States like Rajasthan, UP, Tamil Nadu show steady growth
    - Growing markets with strong potential to reach high value segment
    - Mix of urban and semi urban populations drives moderate volumes
    - Regional language support can significantly boost engagement here
    """)

    st.markdown("#### 🥉 Low Value States")
    st.markdown("""
    - Small northeastern states and union territories
    - Low population density and poor digital infrastructure
    - Cash still dominates daily transactions in these regions
    - Long term growth opportunity with right investment
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - **High Value States:** Retain users with premium loyalty programs and exclusive offers
    - **Medium Value States:** Aggressive merchant onboarding and regional language campaigns
    - **Low Value States:** Digital literacy programs and government partnerships
    - Launch new features in High Value States first before rolling out nationwide
    - Allocate marketing budget proportional to segment revenue potential
    """)

elif menu == "Fraud Detection":
    st.title("🚨 Fraud Detection")
    st.markdown("---")

    # Fetch data
    df_fraud = run_query("""
        SELECT
            state,
            year,
            quarter,
            transaction_type,
            transaction_count,
            transaction_amount,
            transaction_amount / transaction_count AS avg_txn_value
        FROM aggregated_transaction
        WHERE state != 'india'
    """)

    # Calculate thresholds
    mean_amount = df_fraud['transaction_amount'].mean()
    std_amount = df_fraud['transaction_amount'].std()
    mean_avg_value = df_fraud['avg_txn_value'].mean()
    std_avg_value = df_fraud['avg_txn_value'].std()

    threshold_amount = mean_amount + 3 * std_amount
    threshold_value = mean_avg_value + 3 * std_avg_value

    # Flag suspicious
    df_fraud['is_suspicious'] = (
        (df_fraud['transaction_amount'] > threshold_amount) |
        (df_fraud['avg_txn_value'] > threshold_value)
    )

    suspicious = df_fraud[df_fraud['is_suspicious'] == True]
    normal = df_fraud[df_fraud['is_suspicious'] == False]

    # ── KPI Cards ─────────────────────────────────────────
    st.subheader("📊 Fraud Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📋 Total Records", f"{len(df_fraud):,}")
    with col2:
        st.metric("✅ Normal Records", f"{len(normal):,}")
    with col3:
        st.metric("🚨 Suspicious Records", f"{len(suspicious):,}")
    with col4:
        fraud_rate = len(suspicious) / len(df_fraud) * 100
        st.metric("⚠️ Suspicious Rate", f"{fraud_rate:.2f}%")

    st.markdown("---")

    # ── Threshold Info ────────────────────────────────────
    st.subheader("📏 Detection Thresholds Used")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Amount Threshold:** ₹{threshold_amount/1e9:.2f} Billion\n\n"
                f"Transactions above this amount are flagged")
    with col2:
        st.info(f"**Avg Value Threshold:** ₹{threshold_value:,.2f}\n\n"
                f"Transactions with avg value above this are flagged")

    st.markdown("---")

    # ── Scatter Plot ──────────────────────────────────────
    st.subheader("🔍 Suspicious vs Normal Transactions")
    fig = px.scatter(
        df_fraud,
        x='transaction_count',
        y='transaction_amount',
        color='is_suspicious',
        title='Suspicious vs Normal Transactions',
        color_discrete_map={
            True: 'red',
            False: 'green'
        },
        labels={
            'is_suspicious': 'Suspicious',
            'transaction_count': 'Transaction Count',
            'transaction_amount': 'Transaction Amount'
        },
        hover_data=['state', 'year', 'quarter', 'transaction_type']
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Suspicious by State ───────────────────────────────
    st.subheader("🗺️ Suspicious Transactions by State")
    sus_state = suspicious.groupby('state').size().reset_index(name='count')
    sus_state = sus_state.sort_values('count', ascending=False)

    fig = px.bar(
        sus_state,
        x='state',
        y='count',
        color='count',
        color_continuous_scale='Reds',
        title='Number of Suspicious Transactions by State'
    )
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Suspicious by Year ────────────────────────────────
    st.subheader("📈 Suspicious Transaction Trend by Year")
    sus_year = suspicious.groupby('year').size().reset_index(name='count')

    fig = px.line(
        sus_year,
        x='year',
        y='count',
        markers=True,
        color_discrete_sequence=['red'],
        title='Suspicious Transactions by Year'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Suspicious by Transaction Type ───────────────────
    st.subheader("💳 Suspicious Transactions by Type")
    sus_type = suspicious.groupby('transaction_type').size().reset_index(name='count')

    fig = px.pie(
        sus_type,
        names='transaction_type',
        values='count',
        title='Suspicious Transaction Type Distribution',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Suspicious Records Table ──────────────────────────
    st.subheader("📋 Suspicious Transaction Records")
    st.dataframe(
        suspicious[[
            'state', 'year', 'quarter',
            'transaction_type',
            'transaction_count',
            'transaction_amount',
            'avg_txn_value'
        ]].sort_values('transaction_amount', ascending=False),
        use_container_width=True
    )

    st.markdown("---")

    # ── Insights ──────────────────────────────────────────
    st.subheader("💡 Fraud Detection Insights")
    st.markdown("""
    - Transactions with amounts more than 3 standard deviations above mean are flagged
    - Unusually high average transaction values indicate possible account takeover
    - High value states show more suspicious records due to higher overall volumes
    - Q4 festive season shows disproportionately high suspicious transaction rates
    - Peer to Peer payments show the highest number of suspicious transactions
    - Sudden spikes in state level amounts in specific quarters need investigation
    """)

    st.markdown("---")
    st.subheader("✅ Fraud Prevention Recommendations")
    st.markdown("""
    - Implement real time transaction scoring for every payment
    - Add two factor authentication for transactions above ₹50,000
    - Set configurable daily transaction limits per user account
    - Flag transactions from unusual geographical locations
    - Monitor merchant accounts for sudden incoming payment spikes
    - Build machine learning model using Random Forest for real time fraud scoring
    - Send instant alerts to users for any transaction above their average value
    - Temporarily block accounts showing multiple suspicious transactions
    """)
elif menu == "ML Models":
    st.title("🤖 ML Models - Transaction Prediction & Fraud Detection")
    st.markdown("---")

    # Import libraries
    try:
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
        from sklearn.metrics import (mean_absolute_error,
                                     mean_squared_error,
                                     r2_score,
                                     classification_report,
                                     confusion_matrix,
                                     accuracy_score,
                                     roc_auc_score,
                                     roc_curve)
        import numpy as np
    except:
        st.error("Please run: pip install scikit-learn")
        st.stop()

    # ── Load Data ─────────────────────────────────────────
    df = run_query("""
        SELECT
            state,
            year,
            quarter,
            transaction_type,
            transaction_count,
            transaction_amount
        FROM aggregated_transaction
        WHERE state != 'india'
    """)

    # ── Encode Features ───────────────────────────────────
    le_state = LabelEncoder()
    le_type = LabelEncoder()
    df['state_encoded'] = le_state.fit_transform(df['state'])
    df['type_encoded'] = le_type.fit_transform(df['transaction_type'])

    # ── Features and Target ───────────────────────────────
    X = df[[
        'state_encoded',
        'year',
        'quarter',
        'type_encoded',
        'transaction_count'
    ]]
    y = df['transaction_amount']

    # ── Split Data ────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ── Scale Data ────────────────────────────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ── Train Models ──────────────────────────────────────
    with st.spinner("Training ML Models... Please wait..."):

        # Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train_scaled, y_train)
        lr_predictions = lr_model.predict(X_test_scaled)
        lr_mae = mean_absolute_error(y_test, lr_predictions)
        lr_rmse = np.sqrt(mean_squared_error(y_test, lr_predictions))
        lr_r2 = r2_score(y_test, lr_predictions)

        # Random Forest
        rf_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        rf_model.fit(X_train_scaled, y_train)
        rf_predictions = rf_model.predict(X_test_scaled)
        rf_mae = mean_absolute_error(y_test, rf_predictions)
        rf_rmse = np.sqrt(mean_squared_error(y_test, rf_predictions))
        rf_r2 = r2_score(y_test, rf_predictions)

    st.success("Models trained successfully!")

    # ── KPI Cards ─────────────────────────────────────────
    st.subheader("📊 Model Performance Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔵 LR R2 Score",
                  f"{lr_r2:.4f}")
    with col2:
        st.metric("🟣 RF R2 Score",
                  f"{rf_r2:.4f}")
    with col3:
        st.metric("🔵 LR MAE",
                  f"₹{lr_mae/1e6:.2f}M")
    with col4:
        st.metric("🟣 RF MAE",
                  f"₹{rf_mae/1e6:.2f}M")

    st.markdown("---")

    # ── Model Comparison Chart ────────────────────────────
    st.subheader("📊 Model Comparison")
    results = {
        'Model': ['Linear Regression', 'Random Forest'],
        'R2 Score': [lr_r2, rf_r2],
        'MAE': [lr_mae, rf_mae],
        'RMSE': [lr_rmse, rf_rmse]
    }
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.bar(
            df_results,
            x='Model',
            y='R2 Score',
            color='Model',
            title='R2 Score Comparison',
            color_discrete_map={
                'Linear Regression': 'steelblue',
                'Random Forest': 'purple'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            df_results,
            x='Model',
            y='MAE',
            color='Model',
            title='MAE Comparison',
            color_discrete_map={
                'Linear Regression': 'steelblue',
                'Random Forest': 'purple'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = px.bar(
            df_results,
            x='Model',
            y='RMSE',
            color='Model',
            title='RMSE Comparison',
            color_discrete_map={
                'Linear Regression': 'steelblue',
                'Random Forest': 'purple'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Actual vs Predicted ───────────────────────────────
    st.subheader("🎯 Actual vs Predicted - Random Forest")
    fig = px.scatter(
        x=y_test.values / 1e9,
        y=rf_predictions / 1e9,
        labels={
            'x': 'Actual Amount (₹ Billions)',
            'y': 'Predicted Amount (₹ Billions)'
        },
        title='Actual vs Predicted Transaction Amount',
        color_discrete_sequence=['purple']
    )
    fig.add_shape(
        type='line',
        x0=y_test.min() / 1e9,
        y0=y_test.min() / 1e9,
        x1=y_test.max() / 1e9,
        y1=y_test.max() / 1e9,
        line=dict(color='red', width=2, dash='dash')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Feature Importance ────────────────────────────────
    st.subheader("🔍 Feature Importance - Random Forest")
    feature_names = [
        'State',
        'Year',
        'Quarter',
        'Transaction Type',
        'Transaction Count'
    ]
    importances = rf_model.feature_importances_

    df_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=True)

    fig = px.bar(
        df_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Purples',
        title='Feature Importance Scores'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Fraud Detection Section ───────────────────────────
    st.subheader("🚨 Fraud Detection ML Model")

    df_fraud = run_query("""
        SELECT
            state,
            year,
            quarter,
            transaction_type,
            transaction_count,
            transaction_amount,
            transaction_amount / transaction_count AS avg_txn_value
        FROM aggregated_transaction
        WHERE state != 'india'
    """)

    # Create fraud labels
    mean_amount = df_fraud['transaction_amount'].mean()
    std_amount = df_fraud['transaction_amount'].std()
    mean_avg = df_fraud['avg_txn_value'].mean()
    std_avg = df_fraud['avg_txn_value'].std()

    df_fraud['is_fraud'] = (
        (df_fraud['transaction_amount'] > mean_amount + 3 * std_amount) |
        (df_fraud['avg_txn_value'] > mean_avg + 3 * std_avg)
    ).astype(int)

    # Encode
    df_fraud['state_encoded'] = le_state.fit_transform(df_fraud['state'])
    df_fraud['type_encoded'] = le_type.fit_transform(df_fraud['transaction_type'])

    # Features
    X_fraud = df_fraud[[
        'state_encoded',
        'year',
        'quarter',
        'type_encoded',
        'transaction_count',
        'transaction_amount',
        'avg_txn_value'
    ]]
    y_fraud = df_fraud['is_fraud']

    # Split
    X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(
        X_fraud, y_fraud,
        test_size=0.2,
        random_state=42,
        stratify=y_fraud
    )

    # Scale
    scaler_f = StandardScaler()
    X_train_f_scaled = scaler_f.fit_transform(X_train_f)
    X_test_f_scaled = scaler_f.transform(X_test_f)

    # Train
    with st.spinner("Training Fraud Detection Model..."):
        fraud_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        fraud_model.fit(X_train_f_scaled, y_train_f)
        y_pred_fraud = fraud_model.predict(X_test_f_scaled)
        y_prob_fraud = fraud_model.predict_proba(X_test_f_scaled)[:, 1]

    accuracy = accuracy_score(y_test_f, y_pred_fraud)
    auc_score = roc_auc_score(y_test_f, y_prob_fraud)

    st.success("Fraud Detection Model trained!")

    # Fraud KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Accuracy",
                  f"{accuracy*100:.2f}%")
    with col2:
        st.metric("📈 AUC Score",
                  f"{auc_score:.4f}")
    with col3:
        st.metric("🚨 Fraud Records",
                  f"{df_fraud['is_fraud'].sum():,}")
    with col4:
        fraud_rate = df_fraud['is_fraud'].mean() * 100
        st.metric("⚠️ Fraud Rate",
                  f"{fraud_rate:.2f}%")

    st.markdown("---")

    # Confusion Matrix
    st.subheader("🔢 Confusion Matrix")
    cm = confusion_matrix(y_test_f, y_pred_fraud)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Reds',
        xticklabels=['Normal', 'Fraud'],
        yticklabels=['Normal', 'Fraud'],
        ax=ax
    )
    ax.set_title('Confusion Matrix')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    st.pyplot(fig)

    st.markdown("---")

    # ROC Curve
    st.subheader("📈 ROC Curve")
    fpr, tpr, _ = roc_curve(y_test_f, y_prob_fraud)
    fig = px.line(
        x=fpr,
        y=tpr,
        labels={
            'x': 'False Positive Rate',
            'y': 'True Positive Rate'
        },
        title=f'ROC Curve (AUC = {auc_score:.4f})',
        color_discrete_sequence=['purple']
    )
    fig.add_shape(
        type='line',
        x0=0, y0=0, x1=1, y1=1,
        line=dict(color='red', dash='dash')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Fraud Feature Importance
    st.subheader("🔍 Feature Importance - Fraud Detection")
    fraud_features = [
        'State',
        'Year',
        'Quarter',
        'Transaction Type',
        'Transaction Count',
        'Transaction Amount',
        'Avg Transaction Value'
    ]
    fraud_importances = fraud_model.feature_importances_
    df_fraud_imp = pd.DataFrame({
        'Feature': fraud_features,
        'Importance': fraud_importances
    }).sort_values('Importance', ascending=True)

    fig = px.bar(
        df_fraud_imp,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale='Reds',
        title='Fraud Detection Feature Importance'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Insights
    st.subheader("💡 ML Model Insights")
    st.markdown("""
    - Random Forest outperforms Linear Regression for transaction prediction
    - Transaction Count is the most important feature for amount prediction
    - Year is the second most important feature confirming strong growth trend
    - Fraud Detection model achieves high accuracy due to clear statistical patterns
    - Average Transaction Value is the strongest signal for fraud detection
    - Q4 shows highest prediction errors due to festive season anomalies
    - High value states like Maharashtra are harder to predict accurately
    - Fraud rate is very low confirming that PhonePe transactions are mostly legitimate
    """)

    st.markdown("---")
    st.subheader("✅ Business Recommendations")
    st.markdown("""
    - Deploy Random Forest model in production for transaction amount prediction
    - Use fraud detection model to flag suspicious transactions in real time
    - Set up automated alerts when fraud probability exceeds 80%
    - Retrain models quarterly with new transaction data
    - Add more features like user age and device type to improve accuracy
    - Use feature importance to focus data collection on most impactful variables
    """)

# ── Transaction Forecast ──────────────────────────────────
elif menu == "Transaction Forecast":
    st.title("📈 Transaction Growth Forecast")
    st.markdown("---")

    try:
        from sklearn.linear_model import LinearRegression
        import numpy as np
    except:
        st.error("Please run: pip install scikit-learn")
        st.stop()

    # Load yearly data
    df_ts = run_query("""
        SELECT year,
               SUM(transaction_amount) AS total_amount,
               SUM(transaction_count) AS total_count
        FROM aggregated_transaction
        WHERE state = 'india'
        GROUP BY year
        ORDER BY year
    """)

    # Train model
    X_ts = df_ts[['year']]
    y_amount = df_ts['total_amount']
    y_count = df_ts['total_count']

    model_amount = LinearRegression()
    model_amount.fit(X_ts, y_amount)

    model_count = LinearRegression()
    model_count.fit(X_ts, y_count)

    # Forecast
    future_years = pd.DataFrame({'year': [2025, 2026, 2027]})
    pred_amount = model_amount.predict(future_years)
    pred_count = model_count.predict(future_years)

    # ── KPI Cards ─────────────────────────────────────────
    st.subheader("🔮 Forecast Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📅 2025 Forecast",
            f"₹{pred_amount[0]/1e12:.2f} Trillion"
        )
    with col2:
        st.metric(
            "📅 2026 Forecast",
            f"₹{pred_amount[1]/1e12:.2f} Trillion"
        )
    with col3:
        st.metric(
            "📅 2027 Forecast",
            f"₹{pred_amount[2]/1e12:.2f} Trillion"
        )

    st.markdown("---")

    # ── Amount Forecast Chart ─────────────────────────────
    st.subheader("💰 Transaction Amount Forecast")

    actual_df = pd.DataFrame({
        'year': df_ts['year'],
        'amount': df_ts['total_amount'] / 1e12,
        'type': 'Actual'
    })

    forecast_df = pd.DataFrame({
        'year': [2025, 2026, 2027],
        'amount': pred_amount / 1e12,
        'type': 'Forecast'
    })

    combined_df = pd.concat([actual_df, forecast_df])

    fig = px.line(
        combined_df,
        x='year',
        y='amount',
        color='type',
        markers=True,
        title='Transaction Amount - Actual vs Forecast (₹ Trillions)',
        color_discrete_map={
            'Actual': 'blue',
            'Forecast': 'red'
        }
    )
    fig.update_traces(line=dict(width=2))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Count Forecast Chart ──────────────────────────────
    st.subheader("🔢 Transaction Count Forecast")

    actual_count_df = pd.DataFrame({
        'year': df_ts['year'],
        'count': df_ts['total_count'] / 1e9,
        'type': 'Actual'
    })

    forecast_count_df = pd.DataFrame({
        'year': [2025, 2026, 2027],
        'count': pred_count / 1e9,
        'type': 'Forecast'
    })

    combined_count_df = pd.concat([actual_count_df, forecast_count_df])

    fig = px.line(
        combined_count_df,
        x='year',
        y='count',
        color='type',
        markers=True,
        title='Transaction Count - Actual vs Forecast (Billions)',
        color_discrete_map={
            'Actual': 'blue',
            'Forecast': 'red'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Forecast Table ────────────────────────────────────
    st.subheader("📋 Detailed Forecast Table")

    forecast_table = pd.DataFrame({
        'Year': [2025, 2026, 2027],
        'Predicted Amount (₹ Trillions)': [
            f"₹{p/1e12:.2f}T" for p in pred_amount
        ],
        'Predicted Count (Billions)': [
            f"{c/1e9:.2f}B" for c in pred_count
        ],
        'Growth vs 2024': [
            f"{((p - df_ts['total_amount'].iloc[-1]) / df_ts['total_amount'].iloc[-1] * 100):.1f}%"
            for p in pred_amount
        ]
    })

    st.dataframe(forecast_table, use_container_width=True)

    st.markdown("---")

    # ── Year on Year Growth ───────────────────────────────
    st.subheader("📊 Historical Year on Year Growth")

    df_ts['yoy_growth'] = df_ts['total_amount'].pct_change() * 100

    fig = px.bar(
        df_ts.dropna(),
        x='year',
        y='yoy_growth',
        color='yoy_growth',
        color_continuous_scale='RdYlGn',
        title='Year on Year Transaction Growth (%)'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Insights ──────────────────────────────────────────
    st.subheader("💡 Forecast Insights")
    st.markdown("""
    - Transaction amounts are forecast to continue growing strongly through 2027
    - Year on year growth rate shows consistent upward momentum
    - COVID-19 in 2020 caused the biggest single year growth spike
    - Growth is expected to stabilize at a sustainable rate post 2024
    - Transaction count is growing faster than amount showing more small value payments
    - 2025 forecast represents the minimum investment PhonePe needs to handle
    - Forecast assumes no major regulatory changes or market disruptions
    """)

    st.markdown("---")
    st.subheader("✅ Business Planning Recommendations")
    st.markdown("""
    - Use 2025 forecast to plan server capacity and infrastructure investment
    - Use 2026 forecast for medium term hiring and expansion planning
    - Use 2027 forecast for long term strategic decisions
    - Monitor actual vs forecast monthly to detect early signs of deviation
    - Update forecast model every quarter with new transaction data
    - Plan marketing budgets proportional to forecast growth rates
    - Prepare contingency plans if actual growth falls below forecast
    """)