# Messenger Chat Application

## Overview

Messenger is a full-stack chat application that allows users to sign up, log in, and chat in real time. The project demonstrates both real-time and RESTful messaging features. It combines traditional HTTP endpoints with WebSocket support (although you may use either as needed) and integrates multiple backend technologies. The application leverages both SQL (SQLite) and NoSQL (MongoDB) databases, uses Redis for caching, and incorporates Apache Kafka for message streaming. Additionally, Apache Airflow is demonstrated for scheduling background jobs and data management tasks.

## Project Structure

```
Messenger
├── css/
│   └── styles.css          # CSS styles for the application
├── js/
│   └── main.js             # JavaScript code for WebSocket connection / message handling
├── templates/
│   ├── index.html          # Main chat interface (currently demonstrating WebSocket usage)
│   ├── login.html          # Login page for users
│   ├── signup.html         # Sign up page for new user registration
│   ├── welcome.html        # Welcome page (landing page)
│   ├── chats.html          # List of chats with last message and other participant info
│   └── chat.html           # Single chat page (REST implementation)
├── airflow/                # Sample Airflow DAG for scheduled tasks (placed in Airflow DAGs folder)
├── cache.py                # Redis cache configuration and client
├── database.py             # SQLite database setup for SQL models (using SQLAlchemy)
├── mongodb.py              # Motor client for MongoDB (NoSQL)
├── models.py               # SQLAlchemy models (SQLite)
├── models_mongo.py         # Pydantic models for MongoDB-based document validation
├── consumer.py             # Kafka consumer which streams incoming chat messages into MongoDB
├── main.py                 # The FastAPI application containing endpoints (auth, chat, messaging)
├── requirements.txt        # Python dependencies for the project
├── Dockerfile              # Dockerfile for building the project image
└── docker-compose.yml      # Docker Compose file to orchestrate API, consumer, MongoDB, Kafka, Redis, etc.
```

## Files Description

- **Dockerfile**:  
  Defines the container image setup for the FastAPI application and other Python scripts. It installs dependencies from `requirements.txt`, sets environment variables, and exposes port 8000.

- **docker-compose.yml**:  
  Orchestrates multiple containers:
  - `api`: The FastAPI application container.
  - `consumer`: A container running the Kafka consumer.
  - `mongodb`: MongoDB container for NoSQL data storage.
  - `redis`: Redis container used for caching.
  - `zookeeper` and `kafka`: Containers providing Kafka infrastructure for message streaming.

- **requirements.txt**:  
  Lists all required Python packages (FastAPI, Uvicorn, Motor, kafka-python, python-jose, passlib, Redis, Jinja2, SQLAlchemy, etc).

- **airflow**:  
  Contains a sample Airflow DAG (`chat_summary`), intended to be placed in the Airflow DAGs folder, which demonstrates the use of Airflow to schedule background tasks such as aggregating chat data.

- **cache.py**:  
  Configures and initiates a Redis client which is used to cache messages for improved performance.

- **database.py**:  
  Sets up the SQLite database connection and SQLAlchemy models registration (for SQL data).

- **mongodb.py**:  
  Connects to MongoDB using Motor; defines NoSQL collections for users, chats, messages, and user-chats.

- **models.py**:  
  Contains SQLAlchemy ORM models for Users, Chats, and Messages – using SQLite.

- **models_mongo.py**:  
  Provides Pydantic models for MongoDB document validation (for User, Chat, Message, and UserChats).

- **main.py**:  
  The core FastAPI application. It implements endpoints for user authentication (login, signup), token generation, chat and messaging functionalities (both REST based and WebSocket based), and session management via cookies.

- **consumer.py**:  
  A Kafka consumer that listens to a Kafka topic ("chat_messages"), processes incoming messages, and writes them to MongoDB. It also updates chat metadata for later retrieval by the FastAPI app.

- **Templates**:  
  Various HTML templates that are rendered by FastAPI:
  - `login.html`, `signup.html`, and `welcome.html` for authentication and landing.
  - `chats.html` to display a list of available chats, showing each chat’s last message and the other participant’s username.
  - `chat.html` for the detailed view of a specific chat using REST endpoints.

- **js/main.js & css/styles.css**:  
  Provide client-side functionality and styling for the application.

## Setup Instructions with Docker

1. **Clone the Repository**  
   Clone the project repository to your local machine.

2. **Prepare Environment**  
   Ensure Docker is installed on your system. If using Docker Compose V2, you can use the command `docker compose`; otherwise, install docker-compose.

3. **Build and Run Containers**  
   In the project root (where `docker-compose.yml` is located), run:
   ```bash
   docker compose up --build
   ```
   This command will build and start containers for:
   - FastAPI (`api`)
   - Kafka Consumer (`consumer`)
   - MongoDB (`mongodb`)
   - Redis (`redis`)
   - Kafka and Zookeeper (`kafka` & `zookeeper`)

4. **Access the Application**  
   - The FastAPI app is accessible at [http://localhost:8000](http://localhost:8000).  
   - Static HTML pages (login, signup, etc.) can be accessed via their URL if served.
   - Kafka and other containers will run in the background for streaming and caching functionalities.
   - (Airflow is not included in this configuration, but a sample DAG file is provided in the `airflow` folder if needed separately.)

## Usage Guidelines

- **User Authentication**:  
  Users can sign up and log in using the provided forms. The application uses OAuth2 with JWT tokens stored in cookies for authentication.

- **Chat Functionality**:  
  Once logged in, users can:
  - View a list of chats (in `chats.html`), with each chat showing the last message and the other participant’s username.
  - Enter a specific chat page (`chat.html`) to view and send messages.
  - Send messages via REST endpoints (with Kafka publishing to process and integrate messages asynchronously).

- **Data Flow**:  
  - New messages are published to Kafka by the API and consumed by a separate consumer service that writes them to MongoDB.
  - The application leverages caching with Redis to reduce database load.
  - SQLite is used for certain SQL-based operations (for example, storing users and chat metadata via SQLAlchemy), while MongoDB stores messages and enables fast retrieval through NoSQL document structures.

## Used Tools and Concepts

- **Authorization & Authentication**:  
  Implemented using OAuth2PasswordBearer and JWT tokens. Cookies are used to persist the authentication tokens on the client side.

- **WebSocket and REST**:  
  The application contains functionality for both real-time messaging (via WebSocket) and traditional REST endpoints. Although the primary focus can shift between these two mechanisms, REST endpoints are provided for tasks such as posting messages and retrieving chat histories.

- **Caching with Redis**:  
  Redis is used to cache frequently accessed data (like messages) to speed up responses and reduce load on the primary databases.

- **Databases**:  
  - **SQLite**: Utilized (with SQLAlchemy) for managing SQL-based data such as user credentials and chat metadata.
  - **MongoDB**: Used (with Motor) for storing NoSQL data like chat messages and conversation history, which can benefit from flexible document storage.

- **Apache Kafka**:  
  Kafka is integrated to decouple message publishing (from the API) and message processing (by the consumer). This allows high-throughput, real-time streaming of chat messages and scalable asynchronous processing.

- **Apache Airflow**:  
  Although not actively deployed in the docker-compose configuration, a sample DAG is provided to demonstrate how Airflow can be used to schedule and orchestrate tasks (e.g., aggregating chat statistics) independently of real-time message processing.

- **Docker & Docker Compose**:  
  The project is fully containerized. Dockerfile defines the build for the API and consumer, and docker-compose orchestrates the multiple services (API, Consumer, MongoDB, Kafka, Redis, and Zookeeper).

## Future Improvements

- Tighten integration of real-time features and client-side updates (e.g., moving fully to WebSocket or implementing client-side polling).
- Enhance error handling and logging across all services.
- Scale the Kafka consumer and add monitoring tools.
- Further secure the application (e.g., configuring HTTPS and secure token management).
- Integrate Apache Airflow in production for robust scheduling and data maintenance tasks.

---

This README should provide a comprehensive overview of your Messenger Chat Application and be useful both for developers working on the project and for those deploying it with Docker.