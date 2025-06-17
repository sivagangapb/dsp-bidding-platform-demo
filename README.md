# 🧠 Real-Time Bidding DSP Simulation Project

This is a simulation of a **Demand-Side Platform (DSP)** for programmatic advertising. It demonstrates real-time bidding, cloud-native logging, scalable analytics, and automated reporting.

Built as part of an evaluation project, this solution includes:
- A FastAPI-based bid server that receives OpenRTB-style bid requests
- Log ingestion in `.ndjson` format, stored in AWS S3
- Snowflake pipeline for bid analytics using external stages, tables, and scheduled tasks
- Daily bid summary reporting via email (SMTP / Colab)
- Documented mock integration of SNS for scalable notifications

---

## ⚙️ Tech Stack

| Layer            | Tools Used                                              |
|------------------|---------------------------------------------------------|
| API Server       | 🐍 FastAPI, Pydantic                                    |
| Logging          | 📝 NDJSON                                               |
| Cloud            | ☁️ AWS ECS Fargate, ECR, S3                             |
| Analytics        | ❄️ Snowflake (External Stage, Table, Task, SQL CTE)    |
| Notification     | 📬 Email (SMTP via Gmail / Colab) + SNS (documented)    |
| Containerization | 🐳 Docker                                               |
| Automation       | 🛠️ Scheduled tasks, Google Colab Notebook              |

---

## 📌 Features

- ✅ `/bid` endpoint (OpenRTB 2.5-style) via FastAPI
- ✅ Validates and logs incoming bid requests in `.ndjson` format
- ✅ Uploads logs to an S3 bucket (per ECS environment variables)
- ✅ Snowflake reads from S3 using external stages
- ✅ SQL CTE summarizes daily bid counts per domain
- ✅ Snowflake scheduled task runs daily and stores summary
- ✅ Email delivery via Google Colab + Gmail App Password
- ✅ SNS logic documented (not implemented to avoid IAM billing setup)
- ✅ Bonus: Node.js version of API also available

---

## 🚀 How to Run

### 🔧 1. Local Development (FastAPI)

```bash
uvicorn main:app --reload


* Visit: `http://localhost:8000/docs` to access Swagger UI
* Use POST requests to `/bid` using Swagger or Postman

---

### 🐳 2. Dockerized Deployment (Locally)

```bash
docker build -t dsp-api .
docker run -d -p 8000:8000 dsp-api
```

---

### ☁️ 3. Cloud Deployment (AWS ECS + ECR)

* ✅ Build and push Docker image to Amazon ECR
* ✅ Deploy container on ECS Fargate
* ✅ Expose public IP (e.g., `http://<public-ip>:8000/docs`)
* ✅ Bid logs are written to `.ndjson` file and pushed to S3

---

## 📊 Snowflake Analytics

* External stage configured to read `.ndjson` from S3
* SQL queries use `FILE_FORMAT => 'json'` and `METADATA$FILENAME`
* Daily summary generated via CTE and inserted using `MERGE`
* Task is scheduled using CRON (`0 0 * * * UTC`)

### Example:

```sql
SELECT * FROM bid_summary_table
ORDER BY summary_date DESC;
```

---

## 📬 Email Reporting via Google Colab

* A Python script (in Colab) connects to Snowflake
* Queries daily summary from `bid_summary_table`
* Sends formatted result as an email via Gmail SMTP

**.env** includes:

```dotenv
EMAIL_ADDRESS=your@gmail.com
EMAIL_PASSWORD=your_app_password
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
```

📧 **Example Email Summary**

```
📊 Daily Bid Summary (2025-06-17)

example.com       - 5 bids  
news-site.org     - 3 bids  
games.app         - 2 bids  
```

---

## 📢 SNS Integration (Mocked)

While full SNS wasn’t implemented to avoid IAM permission complexity, the flow is documented:

* A topic would be created in SNS (e.g., `BidSummaryNotification`)
* Lambda/SQS/Email subscribers receive a message
* `boto3.client("sns").publish(...)` would be used after task completion

Instead, mock logging + email was used to simulate this.

---

## 📂 Repository Structure

```
dsp_project/
├── main.py                 # FastAPI bid server
├── Dockerfile              # Container config
├── bid_requests.ndjson     # Logs
├── dsp_email_report/
│   ├── daily_email.py      # Colab/SMTP script
│   └── .env                # Env variables (private)
├── node_version/           # Node.js implementation
└── README.md               # Project documentation
```

---

## ✅ Evaluation Highlights

* Full-stack project using FastAPI + AWS + Snowflake
* Real-time API + Logging + Analytics + Reporting
* Multiple tech layers & thoughtful integration
* Easily extendable to real-world DSP/SNS pipelines

---


## 🏁 Conclusion

This project demonstrates an end-to-end **DSP simulation pipeline** with modern cloud technologies and real-time analytics — ideal for showcasing cloud-native engineering and system design skills.

```


