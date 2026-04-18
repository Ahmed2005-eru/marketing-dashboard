import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="Marketing Dashboard", layout="wide")

st.title("📊 Marketing Campaign Dashboard")
st.caption("NovaTrust Bank | Final Business Analytics Project")

# =====================
# LOAD DATA
# =====================
@st.cache_data
def load_data():
    return pd.read_csv("bank-additional-full.csv", sep=';')

df = load_data()
df_original = df.copy()

# =====================
# SIDEBAR
# =====================
st.sidebar.header("🔎 Filters")

job = st.sidebar.multiselect("Job", df['job'].unique(), df['job'].unique())
month = st.sidebar.multiselect("Month", df['month'].unique(), df['month'].unique())

if st.sidebar.button("Reset Filters"):
    st.session_state.clear()
    st.rerun()

df = df[(df['job'].isin(job)) & (df['month'].isin(month))]

# =====================
# KPIs
# =====================
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

conversion = (df['y'] == 'yes').mean()

col1.metric("Total Calls", len(df))
col2.metric("Conversion Rate", f"{conversion*100:.2f}%")
col3.metric("Avg Duration", f"{df['duration'].mean():.0f}s")
col4.metric("Avg Contacts", f"{df['campaign'].mean():.2f}")

# =====================
# TABS
# =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Performance",
    "💰 Budget Analysis",
    "🔍 Deep Dive",
    "💡 Insights & Recommendations"
])

# =====================
# TAB 1: PERFORMANCE
# =====================
with tab1:

    st.subheader("👔 Conversion by Job")
    job_conv = pd.crosstab(df['job'], df['y'], normalize='index')['yes']
    st.plotly_chart(px.bar(job_conv.sort_values(),
                          orientation='h',
                          title="Conversion Rate by Job"),
                    use_container_width=True)

    st.subheader("📅 Conversion by Month")
    month_conv = pd.crosstab(df['month'], df['y'], normalize='index')['yes']
    st.plotly_chart(px.bar(month_conv,
                          title="Conversion Rate by Month"),
                    use_container_width=True)

    st.subheader("⏱️ Call Duration Impact")
    st.plotly_chart(px.box(df, x="y", y="duration", color="y"),
                    use_container_width=True)

# =====================
# TAB 2: BUDGET
# =====================
with tab2:

    st.subheader("📞 Calls Distribution (Where Money Goes)")
    st.plotly_chart(px.bar(df['job'].value_counts(),
                          title="Number of Calls per Job"),
                    use_container_width=True)

    st.subheader("🔁 Contact Attempts Effect")
    st.plotly_chart(px.box(df, x="y", y="campaign", color="y"),
                    use_container_width=True)

    st.subheader("📞 Contact Channel Performance")
    contact = pd.crosstab(df['contact'], df['y'], normalize='index')['yes']
    st.plotly_chart(px.bar(contact,
                          title="Conversion by Contact Type"),
                    use_container_width=True)

# =====================
# TAB 3: DEEP DIVE
# =====================
with tab3:

    st.subheader("🔥 Previous Campaign Effect")
    pout = pd.crosstab(df['poutcome'], df['y'], normalize='index')['yes']
    st.plotly_chart(px.bar(pout,
                          title="Conversion by Previous Outcome"),
                    use_container_width=True)

    st.subheader("📊 Compare Full vs Filtered Data")

    full_conv = (df_original['y'] == 'yes').mean()
    filtered_conv = (df['y'] == 'yes').mean()

    comp = pd.DataFrame({
        "Dataset": ["Full Data", "Filtered"],
        "Conversion": [full_conv, filtered_conv]
    })

    st.plotly_chart(px.bar(comp, x="Dataset", y="Conversion",
                          title="Before vs After Filters"),
                    use_container_width=True)

# =====================
# TAB 4: INSIGHTS
# =====================
# BUSINESS STORY
# =====================
st.header("🧠 Business Story")

# Calculate dynamic insights
top_job = pd.crosstab(df['job'], df['y'], normalize='index')['yes'].idxmax()
top_month = pd.crosstab(df['month'], df['y'], normalize='index')['yes'].idxmax()
best_channel = pd.crosstab(df['contact'], df['y'], normalize='index')['yes'].idxmax()

avg_yes_duration = df[df['y'] == 'yes']['duration'].mean()
avg_no_duration = df[df['y'] == 'no']['duration'].mean()

# Story text
st.markdown(f"""
### 📌 What is really happening?

- Customers in **{top_job}** show the highest engagement with the campaign  
- The best performing period is **{top_month}**, indicating strong seasonal behavior  
- **{best_channel}** is the most effective communication channel  

### 🎯 Customer Behavior

- Customers who convert tend to stay longer on calls  
- Average successful call duration ≈ **{avg_yes_duration:.0f} sec**  
- Average unsuccessful call duration ≈ **{avg_no_duration:.0f} sec**

👉 This suggests that engagement level is a key driver of success  

### 💰 Budget Efficiency Problem

- A large portion of calls is spent on low-performing segments  
- High-performing segments are under-targeted  

👉 This creates **inefficient budget allocation**

### 🧠 Business Interpretation

- High-performing segments (like students/retired) are more financially receptive  
- Seasonal peaks indicate better timing opportunities  
- Mobile communication increases reach and responsiveness  
- Repeated calls do not improve conversion → wasted cost  

---

## 🚀 What should the business do?

### ✔ Focus:
- Target **high-conversion segments**
- Retarget **previous successful clients**

### ✔ Optimize:
- Shift campaigns to **high-performing months**
- Use **mobile as primary channel**

### ✔ Reduce Waste:
- Limit repeated calls
- Reduce spending on low-performing segments

---

## 💡 Final Conclusion

> The issue is not the campaign itself —  
> **the issue is how the budget is distributed.**

👉 By reallocating resources, the bank can significantly increase ROI  
without increasing total cost.
""")
# =====================
with tab4:

    st.header("💡 Key Insights")

    st.success("🎯 Students & Retired = Highest Conversion")
    st.success("📅 March & December = Peak Performance")
    st.success("📞 Mobile Channel = ~3x Better")

    st.warning("🔁 Too Many Calls = Waste of Budget")
    st.warning("📉 Blue-collar Segment = Low ROI")

    st.info("🔥 Previous Success Clients = Highest Potential (~65%)")

    st.header("🚀 Recommendations")

    st.markdown("""
    ### 🎯 Targeting
    - Focus on **Students & Retired**
    - Retarget **previous successful clients**

    ### ⏰ Timing
    - Invest more in **March & December**
    - Reduce campaigns in **summer months**

    ### 📞 Strategy
    - Prioritize **Mobile over Telephone**
    - Limit contact attempts to **2–3 max**

    ### 💰 Budget Optimization
    - Shift budget from low-performing segments
    - Focus on high-conversion segments
    """)

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("Built by Ahmed Nasr | Business Analytics Project 🚀")