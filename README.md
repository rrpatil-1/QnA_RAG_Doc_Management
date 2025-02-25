# QnA_RAG_Doc_Management

## Overview
This project is a Question and Answer (QnA) system that uses Retrieval-Augmented Generation (RAG) to provide answers based on the context retrieved from a vector database. The system uses PostgreSQL with the pgvector extension for vector storage and Ollama for language model processing.

## Prerequisites
- Docker
- Python 3.12 or higher
- AWS account (for deployment)

## Setup

### 1. Clone the Repository
```sh
git clone https://github.com/rrpatil-1/QnA_RAG_Doc_Management.git
cd QnA_RAG_Doc_Management
```

### 2. Install Docker
If Docker are not installed, follow these steps:

#### Docker Installation
- **Windows:** Download and install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Mac:** Download and install Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Linux:** Follow the instructions on [Docker's official documentation](https://docs.docker.com/engine/install/).


### 3. Create and Configure the `.env` File
Create a `.env` file in the root directory and add the following environment variables or edit exsting file:

edit the environment variable according to model choose for embedding and database configuration setup in docker_compose.yaml file
```
# Default postgres connectio details
PASSWORD_POSTGRES =postgres
USERNAME_POSTGRES =postgres
DATABASE_POSTGRES =vectordb
HOST_POSTGRES =localhost
PORT_POSTGRES =5432
SCHEMA_POSTGRES =RAG

#llm connection details
ollama_model = llama3.1:8b
# ollama_model=deepseek-r1:1.5b
ollama_url = http://localhost:11434
LLM_MAX_TOKENS=100
LLM_TEMPERATURE=0.7

#text embedding details
collection_name=QnA_RAG
table_name=langchain_pg_embedding
DOC_LIMIT=10
EMBEDDING_BATCH_SIZE=50
embedding_size=4096
```

### 4. Update the Dockerfile
Ensure your Dockerfile is correctly set up to build the backend service. Here is an example:
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the backend code into the container at /app
COPY backend /app/backend
COPY app.py /app/app.py

# Copy the .env file into the container
COPY .env .env

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5. Update the `docker-compose.yaml` File
Ensure your `docker-compose.yaml` file is correctly set up to run the services. Here is an example:
```yaml
# filepath: /deployment/docker_compose.yaml
version: '3.8'

services:
  pgvector:
    image: pgvector/pgvector:pg17
    container_name: pgvector
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: vectordb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d vectordb"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
    networks:
      - pg-network

  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    environment:
      OLLAMA_ORIGINS: "http://localhost:3000"
    command: ["ollama", "run", "llama3.1:8b"]
    networks:
      - pg-network

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: QnARAG
    env_file:
      - .env
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    networks:
      - pg-network
    
volumes:
  pgdata:

networks:
  pg-network:
    driver: bridge
```

### 6. Build and Run the Docker Containers
```sh
docker-compose up --build
```

## API Documentation

### 1. Get Answer
**Endpoint:** `POST /qa_service`

`filter` allows you to select the file once ingested

**Request Body:**
```json
{
  "message": "What is the attention mechanism in neural networks?"
  "filter":""
  
}
```

**Response:**
```json
{
  "response": "The attention mechanism in neural networks..."
}
```

### 2. ingest_documents
**Endpoint:** `POST /ingest_documents`

**Request Body:**
```json
{
  "filepath": "string"
}
```

**Response:**
```json
{"message": "Documents ingested successfully","status":200}
```

## Deployment on AWS

# Deployment on AWS Elastic Beanstalk
1. Create account on AWS [watch video](https://www.youtube.com/watch?v=xi-JDeceLeI).
2. Create IAM role and assign the following policies.
   - AWSElasticBeanstalkWebTier
   - AWSElasticBeanstalkWorkerTier
   - AWSElasticBeanstalkMulticontainerDocker
    
3. Follow the step given in this link [step to create environment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.CreateApp.html).
4. connect git hub with aws using codepipeline [codepipeline](https://www.youtube.com/watch?v=4tDjVFbi31o)
5. Documents for codepipeline [doc](https://aws.amazon.com/getting-started/hands-on/continuous-deployment-pipeline/)


## Response Using API endpoint
1. Download the postman application to test the api [postman](https://www.postman.com/downloads/)

### 7. Monitor and Scale
Monitor the services using CloudWatch and scale the services as needed.

## Conclusion
This README provides a comprehensive guide to setting up, running, and deploying the QnA_RAG_Doc_Management application. Follow the steps carefully to ensure a smooth setup and deployment process.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
