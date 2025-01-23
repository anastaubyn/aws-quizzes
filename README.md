# Streamlit App in Docker

This repository contains a Streamlit app containerized with Docker. The app allows users to interact with a Streamlit interface designed for various use cases.

## Prerequisites

Before running the app, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Python](https://www.python.org/) (if you plan to run the app locally without Docker)

---

## How to Run the App with Docker

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/anastaubyn/aws-quizzes.git
cd app
```

### 2. Build the Docker Image
Use the following command to build the Docker image:
```bash
docker build -t streamlit-app .
```

### 3. Run the Docker Container
Start the container using:
```bash
docker run -p 8501:8501 streamlit-app
```

### 4. Access the App
Open your browser and navigate to:
```bash
http://localhost:8501
```

You should see the Streamlit app interface.