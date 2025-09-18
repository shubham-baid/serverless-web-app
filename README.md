# 🚀 Serverless Web Application with DynamoDB and AWS Lambda

This project demonstrates a simple **serverless CRUD web application** built using:

- **DynamoDB** for database storage  
- **AWS Lambda** for serverless compute  
- **API Gateway** for exposing REST APIs  

---

## 📌 DynamoDB Table Creation

![DynamoDB Table](images/Screenshot%202025-09-17%20at%205.11.56 PM.png)

---

## ⚡ Lambda Function Creation & Code Deployment

![Lambda Creation](images/Screenshot%202025-09-17%20at%205.12.14 PM.png)

![Lambda Code](images/Screenshot%202025-09-17%20at%205.12.34 PM.png)

---

## 🌐 API Gateway: API Creation & Deployment

![API Deployment](images/Screenshot%202025-09-17%20at%205.10.47 PM.png)

![API Methods](images/Screenshot%202025-09-17%20at%205.10.34 PM.png)

---

## 🛠️ CRUD Operations via Postman

- **Create / Insert Item**  
  ![Create Item](images/Screenshot%202025-09-17%20at%205.06.45 PM.png)

- **Read / Get Item**  
  ![Read Item](images/Screenshot%202025-09-17%20at%205.09.07 PM.png)

- **Update Item**  
  ![Update Item](images/Screenshot%202025-09-17%20at%205.09.48 PM.png)

- **Delete Item**  
  ![Delete Item](images/Screenshot%202025-09-17%20at%205.10.21 PM.png)

---

## 💡 Reflection

I didn’t find the assignment itself particularly difficult; the bigger gaps were items not covered in the rubric—such as creating the IAM role and permissions, deploying code to Lambda, and wiring up API Gateway (methods, stages, and CORS). Those missing steps led me to use ChatGPT for the precise sequence. Once those were clear, the core tasks—creating the DynamoDB table, writing the Lambda function, and exposing it through API Gateway—were straightforward.

What I liked about the serverless approach is how much busywork it cuts out. I didn’t have to spin up servers, patch anything, set up Nginx, worry about capacity, or fuss with system packages. I just wrote the function and hit ‘Deploy’. This assignment gave me hands-on time with three core services (DynamoDB, Lambda, API Gateway) and made the AWS console feel a lot less mysterious. Having a clear, end-to-end path to follow was the difference between poking around aimlessly and getting something working quickly.
