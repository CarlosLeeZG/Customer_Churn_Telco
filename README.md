#Deployment of Customer Churn Prediction Model 
Objectives:
- Build a machine learning (ML) binary classifier that predicts the archetypes of clients that are likely to churn
- Deploy the ML binary classifer as a Flask web application hosted on AWS

## Author:
Carlos Lee Zhen Guang

## URLs to Deployed Flask Web Application

App on AWS: http://ec2-47-129-40-17.ap-southeast-1.compute.amazonaws.com

Repo on Docker: [https://hub.docker.com/r/carlosleezg/ai300capstone](https://hub.docker.com/repository/docker/carlosleezg/telco_cust_churn/general)


## Details on chosen CatBoost Classifier and its underlying hyperparameters

| Hyperparameter     | Value  |
|--------------------|--------|
| Max Depth          | 8      |
| Learning Rate      | 0.5    |
| Iterations         | 800    |



## Offline AUC metric of CatBoost Classifier
AUC = <u>0.9445</u>

![image](https://github.com/user-attachments/assets/d4388263-2690-447c-9e40-fbc20e9f9793)
