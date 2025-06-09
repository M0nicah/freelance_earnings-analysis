#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


data=pd.read_csv("freelancer_earnings_bd.csv")
data.head(5)


data.columns


data.isna().sum()


data.isnull().sum()


data.isnull().values.any()


data.duplicated().sum()


data.describe(include="all")


#duplicate rows
data[data.duplicated()]


data.head()


data['Earnings_per_job'] = (data["Earnings_USD"]/ data['Job_Completed']).round(2)


data.head()


#selecting the top earners
top_earners = data.sort_values(by='Earnings_USD', ascending=False)
top_earners.head(10)


top_earners_selected=top_earners[["Freelancer_ID", 'Experience_Level', "Earnings_USD", "Job_Category", "Job_Completed", "Platform"]]
top_earners_selected.head()


#top category by earnings
top_categories= (data.groupby("Job_Category")['Earnings_USD']
.sum()
.sort_values(ascending=False)
.reset_index())
top_categories.columns = ["Job_Category", "Total_Earnings_USD"]
top_categories.head()


#top earning platforms
top_platforms = (data.groupby("Platform")["Earnings_USD"]
                 .sum()
                 .sort_values(ascending=False)
                 .reset_index())

top_platforms.columns = ["Platform", "Total_Earnings_USD"]
top_platforms.head()


#Average Hourly Rate by Experience Level
avg_rate_by_experience = (data.groupby("Experience_Level")
              .agg(
                  avg_hourly_rate = ("Hourly_Rate", 'mean')
                  
              )
                .round(2)
                .sort_values(by='avg_hourly_rate', ascending=False)
                .reset_index()
              )
avg_rate_by_experience.columns=["Experience_Level", "Average_Rate"]

avg_rate_by_experience.head()




#platforms with highest average earnings and success rates.
avg_earnings_and_success_rate = (data.groupby("Platform")
                                    .agg(
                                     avg_earnings = ("Earnings_USD", 'mean'),
                                     avg_success_rate = ("Job_Success_Rate", 'mean')
                                    )
                                    .round(2)
                                    .sort_values(by="avg_earnings", ascending=False)
                                    .reset_index()
                                )
avg_earnings_and_success_rate.columns = ["Platforms", "Average_Earnings", "Average_Success_Rate"]
avg_earnings_and_success_rate.head()


#how client ratings vary by region or payment method
client_rating_by_region = (data.groupby(["Client_Region", "Payment_Method"])
                           .agg(
                               avg_rating = ("Client_Rating", "mean")
                           )
                           .round(2)
                           .sort_values(by="avg_rating", ascending=False)
                           .reset_index()
                           )
client_rating_by_region.columns=["Client_Region", "Payment_Method", "Average_Rating"]
client_rating_by_region.head(10)


##how client ratings vary by payment method
client_rating_by_payment_method = (data.groupby("Payment_Method")
                           .agg(
                               avg_rating = ("Client_Rating", "mean")
                           )
                           .round(2)
                           .sort_values(by="avg_rating", ascending=False)
                           .reset_index()
                           )
client_rating_by_payment_method.columns=["Payment_Method", "Average_Rating"]
client_rating_by_payment_method.head()


#Are expert freelancers significantly more successful in terms of earnings or ratings than beginners or intermediates?

expert_success = (data.groupby("Experience_Level")
                  .agg(
                      total_earnings=("Earnings_USD", "sum"),
                      avg_rating = ("Client_Rating", "mean")
                  )
                  .round(2)
                  .sort_values(by="avg_rating", ascending=False)
                  .reset_index()
                  
                  )
expert_success.columns =["Experience_Level", "Total_Earnings", "Average_Rating"]
expert_success.head()

# no, experts are only significantly successfull than beginners in terms of success rate and earnings


#Rehire Rate Trends by Client Region
data.groupby('Client_Region')['Rehire_Rate'].mean().round(2).reset_index().sort_values(by='Rehire_Rate', ascending=False).head(10)





#plotting top platforms

plt.figure(figsize=(10,6))
sns.barplot(data=top_platforms, x="Platform", y="Total_Earnings_USD",hue="Platform", palette="twilight")
plt.title = ("Top Platforms")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# plotting average earnings
plt.figure(figsize=(9,5))
sns.barplot(data=avg_earnings_and_success_rate, x="Platforms", y="Average_Earnings", palette="twilight")
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()


#plotting average hourly rate
plt.figure(figsize=(5,6))
sns.barplot(data=avg_rate_by_experience, x="Experience_Level", y="Average_Rate", hue="Platform", palette="twilight")
plt.show()


#spread & skew in freelancer income.
sns.histplot(data['Earnings_USD'], bins=30, kde=True)
plt.show()


#plotting client
sns.barplot(data=data, x='Client_Region', y='Rehire_Rate', estimator='mean', hue="Platform", palette="twilight")
plt.xticks(rotation=45)


#relationship btwn Success Rate & Client Rating colored by experience level
plt.figure(figsize=(10,5))
sns.scatterplot(data=data, x='Job_Success_Rate', y='Client_Rating', hue="Experience_Level")


#Hourly vs Fixed Projects: Earnings Comparison
sns.boxplot(data=data, x='Project_Type', y='Earnings_USD')


#Count Plot: Projects by Client Region
sns.countplot(data=data, x='Client_Region', hue="Platform", palette="twilight")


#Scatter Plot: Marketing Spend vs Earnings to Test if high spend leads to more income.
plt.figure(figsize=(10,6))
sns.scatterplot(data=data, x='Marketing_Spend', y='Earnings_USD', hue='Platform')


#plot top job categories
plt.figure(figsize=(10,6))
sns.barplot(data=top_categories, x='Job_Category', y='Total_Earnings_USD', hue="Platform",  palette="twilight")
plt.xticks(rotation=30)





