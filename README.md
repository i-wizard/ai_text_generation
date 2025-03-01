# AI Text Generator API

## Overview
AI Text Generator API is a Flask-based backend service that allows users to generate and store AI-generated text using OpenAI's language models. The application uses  the Service Layer Design Pattern combined with the Repository Design Pattern.

## Features
- **User Authentication** (Registration & Login using JWT)
- **AI Text Generation** (Supports multiple AI providers, with OpenAI as default)
- **Database Storage** (PostgreSQL + SQLAlchemy)
- **Dependency Injection** (For better modularity & testing)
- **Swagger API Documentation**
- **Automated Database Migrations**
- **Containerization with Docker & Docker Compose**

---

## **Getting Started**

### Set Up Environment Variables**
Create a **`.env`** file in the root directory and define the following environment variables:
```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
OPENAI_API_KEY=your_openai_api_key
```
## **Running with Docker**
### **1. Build and Start the Containers**
```bash
docker compose up --build
```
- The app will be available at: **`http://localhost:5001`**
- Logs can be viewed using:
  ```bash
  docker logs -f <container_id>
  ```

### **2. Stopping the Containers**
```bash
docker compose down
```

### **3. Running Database Migrations in Docker**
```bash
docker-compose exec app flask db init
docker-compose exec app flask db migrate -m "Initial migration"
```
- The API will be available at: **`http://localhost:5001`**
- Swagger API Docs: **[http://localhost:5001/docs](http://localhost:5001/docs)**

---

## **Running Tests**

### **1. Run All Tests**
```bash
pytest
```

## **Author**
[David Njoagwuani]
