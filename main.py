import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(layout='wide',page_title="EduPro Learner Analytics",page_icon="📚")

st.title("EduPro Learner Demographics & Course Enrollment Dashboard")
st.markdown("----")

def load_data():
    file_path=r"C:/Users/DELL/Documents/EduPro Learner Intelligence Dashboard Demographics & Course Enrollment Analytics/merged_data.csv"
    df=pd.read_csv(file_path)
    df['TransactionDate']=pd.to_datetime(df['TransactionDate'])
    return df
try:
    df=load_data()
    st.success(f"Loaded {len(df)} Records")
except FileNotFoundError:
    st.error("Pkease run merge_data.csv to create merged_data.csv")
    st.stop()

st.sidebar.header("Filter Data")

min_date=df['TransactionDate'].min()
max_date=df['TransactionDate'].max()
date_range=st.sidebar.date_input(
    "Date Range",
    value=[min_date,max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range)==2:
    start_date,end_date=date_range
    df=df[(df['TransactionDate']>=pd.to_datetime(start_date))&
          (df['TransactionDate']<=pd.to_datetime(end_date))]

age_bands=st.sidebar.multiselect(
    "Age Groups",
    options=sorted(df['AgeBand'].unique()),
    default=sorted(df['AgeBand'].unique())
)

genders=st.sidebar.multiselect(
    "Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

categories=st.sidebar.multiselect(
    "Courses Category",
    options=sorted(df["CourseCategory"].unique()),
    default=sorted(df["CourseCategory"].unique())
)

levels=st.sidebar.multiselect(
    "Courses Level",
    options=df['CourseLevel'].unique(),
    default=df['CourseLevel'].unique()
)


df_filtered=df[
    df['AgeBand'].isin(age_bands)&
    df['Gender'].isin(genders)&
    df['CourseCategory'].isin(categories)&
    df['CourseLevel'].isin(levels)
]


col1,col2,col3,col4=st.columns(4)

with col1:
    total_records=len(df_filtered)
    st.metric("Total Records:",f"{total_records:,}")

with col2:
    unique_learners=df_filtered['UserID'].nunique()
    st.metric("Unique Learners:",f"{unique_learners:,}")

with col3:
    avg_courses=total_records/unique_learners if unique_learners>0 else 0
    st.metric("Avg Courses/Learner",f"{avg_courses:.1f}")

with col4:
    female_count=df_filtered[df_filtered['Gender']=='Female']['UserID'].nunique()
    male_count=df_filtered[df_filtered['Gender']=='Male']['UserID'].nunique()
    gender_ratio=female_count/male_count if male_count>0 else 0
    st.metric("Gender Ratio",f"{gender_ratio:.2f}")

st.markdown("----")

col1,col2=st.columns(2)

with col1:
    st.subheader("Age Distribution of Learners")
    unique_learner_age=df_filtered.drop_duplicates('UserID')[['Age','UserID']]
    hist_age=px.histogram(
        unique_learner_age,
        x="Age",
        nbins=30,
        title="Learner Age Distribution",
        color_discrete_sequence=['#2E86AB']

    )
    st.plotly_chart(hist_age,use_container_width=True)

with col2:
    st.subheader("Records by Age Group")
    enroll_by_age=df_filtered.groupby('AgeBand').size().reset_index(name='Enrollments')
    age_order = ['Under 18', '18-25', '26-35', '36-45', '45+', 'Unknown']
    enroll_by_age['AgeBand']=pd.Categorical(enroll_by_age['AgeBand'],categories=age_order,ordered=True)
    enroll_by_age=enroll_by_age.sort_values('AgeBand')
    bar_age=px.bar(
        enroll_by_age,
        x='AgeBand',
        y='Enrollments',
        title='Total Enrollments by Age Band',
        color='Enrollments',
        color_continuous_scale='Blues',
    )
    st.plotly_chart(bar_age,use_container_width=True)

st.markdown("----")

st.subheader("Gender vs Course Category Preference")
gender_category=pd.crosstab(df_filtered['Gender'],df_filtered['CourseCategory'])
heatmap_gender=px.imshow(
    gender_category,
    text_auto=True,
    title='Enrollment Count: Gender vs Course Category',
    color_continuous_scale='Reds'
)
st.plotly_chart(heatmap_gender,use_container_width=True)

st.markdown("----")

col1,col2=st.columns(2)

with col1:
    st.subheader("Most Popular Course Categories")
    category_pop=df_filtered['CourseCategory'].value_counts().reset_index()
    category_pop.columns=['Category','Enrollments']
    cat_bar=px.bar(
        category_pop,
        x='Enrollments',
        y='Category',
        title='Enrollments by Categories',
        color='Enrollments',
        color_continuous_scale='Greens',
        orientation='h'
    )
    st.plotly_chart(cat_bar,use_container_width=True)

with col2:
    st.subheader("Course Level Distribution")
    level_dist=df_filtered['CourseLevel'].value_counts().reset_index()
    level_dist.columns=['Level','Enrollments']
    level_pie=px.pie(
        level_dist,
        values='Enrollments',
        names='Level',
        title='Enrollment by Course Level',
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
    )
    st.plotly_chart(level_pie,use_container_width=True)

st.markdown("----")

st.subheader("Course Category Preferences by Age Group")
age_category=pd.crosstab(df_filtered['AgeBand'],df_filtered['CourseCategory'])
age_category=age_category.reindex(age_order,fill_value=0)
stacked_bar=px.bar(
    age_category,
    barmode='stack',
    title='Course Category Across Age Groups',
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(stacked_bar,use_container_width=True)

st.markdown("----")

st.subheader("Free vs Paid Course Enrolment")
df_filtered['PriceType']=df_filtered['CoursePrice'].apply(lambda x:'Free' if x == 0 else 'Paid')
price_by_age=pd.crosstab(df_filtered['AgeBand'],df_filtered['PriceType'])
price_by_age=price_by_age.reindex(age_order,fill_value=0)
price_bar=px.bar(
    price_by_age,
    barmode='group',
    title='Free vs Paid Course Enrollment by Age Group',
    color_discrete_sequence=['#2ECC71', '#E74C3C']
)
st.plotly_chart(price_bar,use_container_width=True)

st.markdown("----")

st.subheader("Detailed Enrollment Data")
st.dataframe(df_filtered[['UserID', 'Age', 'Gender', 'AgeBand', 'CourseName', 'CourseCategory', 'CourseLevel', 'CoursePrice', 'TransactionDate']].head(100),
             use_container_width=True
)

st.markdown("----")

csv=df_filtered.to_csv(index=False)
st.download_button(
    label='Download Filtered Data as CSV',
    data=csv,
    file_name='edupro_filtered_data.csv',
    mime='text/csv'
)
st.markdown('----')