# Intelligent Job Aggregation & Recommendation Platform

A production-oriented job aggregation platform built with Python that collects job listings from multiple public APIs and RSS feeds, processes and deduplicates them, categorizes them by skills and technologies, and eventually uses machine learning to provide personalized job recommendations.

The project starts as a **concurrent Python CLI application** and progressively evolves into a full-stack platform with a **FastAPI backend, PostgreSQL database, Redis/Celery background workers, machine-learning recommendation system, and React frontend**.

---

## 📌 Project Status

> 🚧 **Currently under development**

The project is being developed incrementally. Features are introduced in stages so that each part of the system can be properly designed, tested, and understood before moving to the next level.

### Development roadmap

* [ ] Project foundation
* [ ] Job domain model
* [ ] Job source abstraction
* [ ] First API source
* [ ] Multiple job sources
* [ ] Concurrent fetching
* [ ] Data normalization
* [ ] Exact deduplication
* [ ] Near-duplicate detection
* [ ] Keyword-based tagging
* [ ] CLI interface
* [ ] CSV/JSON exporting
* [ ] PostgreSQL persistence
* [ ] Redis + Celery workers
* [ ] Scheduled aggregation
* [ ] FastAPI REST API
* [ ] Authentication and user accounts
* [ ] React frontend
* [ ] TF-IDF job similarity
* [ ] Machine-learning relevance classification
* [ ] Semantic embeddings
* [ ] Personalized recommendations
* [ ] Automated testing
* [ ] Docker
* [ ] CI/CD
* [ ] Production deployment

---

# 🎯 Project Goals

The main goal is to build a real-world system that demonstrates how a Python application can evolve from a simple CLI tool into a production-oriented distributed application.

The project focuses on:

* Concurrent network operations
* API and RSS integration
* Data normalization
* Duplicate detection
* Natural-language processing
* Machine learning
* REST API development
* Background task processing
* Database design
* Caching
* Authentication
* Testing
* Containerization
* CI/CD
* Production deployment

The project is also intended as an educational exercise in **software architecture and machine learning**, rather than simply being a job scraper.

---

# 💡 What Does It Do?

The system collects job listings from multiple sources.

```text
Job APIs
   │
RSS feeds
   │
   ▼
Concurrent Fetching
   │
   ▼
Normalization
   │
   ▼
Deduplication
   │
   ▼
Keyword / Skill Tagging
   │
   ▼
Storage
   │
   ▼
Search / Filtering / Ranking
   │
   ▼
Recommendations
```

For example, the same job may appear on several different job boards.

Instead of showing the user:

```text
Python Developer - Company X
Python Developer - Company X
Senior Python Developer - Company X
Python Backend Developer - Company X
```

the system attempts to determine that these listings represent the same or nearly identical job and keep a single clean record.

---

# 🏗️ Architecture

The final system is designed as a **modular monolith with background workers**.

Microservices are intentionally avoided initially because they would introduce unnecessary operational complexity.

The system is designed so that individual components remain modular and can be separated later if there is a real need.

```text
                         ┌──────────────────┐
                         │     React UI     │
                         │  Tailwind CSS    │
                         └────────┬─────────┘
                                  │
                                HTTPS
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   FastAPI API    │
                         │                  │
                         │ Authentication   │
                         │ Jobs             │
                         │ Search           │
                         │ Users            │
                         │ Recommendations │
                         └───────┬──────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
            PostgreSQL        Redis          ML/Ranking
                 │               │                │
                 │               ▼                │
                 │          Task Queue            │
                 │               │                │
                 │       ┌───────┼───────┐        │
                 │       ▼       ▼       ▼        │
                 │    Worker   Worker   Worker     │
                 │       │       │       │        │
                 │       └───────┼───────┘        │
                 │               │                │
                 │               ▼                │
                 │        Job Sources             │
                 │        ┌────┼────┐             │
                 │        ▼    ▼    ▼             │
                 │       API  API  RSS             │
                 │                                  │
                 └──────────────────────────────────┘
```

---

# 🧱 Architectural Layers

The application is divided into several logical layers.

```text
Presentation
     ↓
Application
     ↓
Domain
     ↓
Infrastructure
     ↓
External Systems
```

## Presentation

Interfaces through which users or external systems interact with the application.

Current:

* CLI

Planned:

* FastAPI REST API
* React frontend

---

## Application

Contains the application's use cases and orchestration logic.

Examples:

* Aggregate jobs
* Search jobs
* Process jobs
* Generate recommendations
* Export jobs

---

## Domain

Contains the core business concepts.

Examples:

* Job
* Company
* Source
* Tag
* User
* User profile
* Recommendation

The domain should not depend on external APIs or frontend code.

---

## Infrastructure

Responsible for technical implementations such as:

* HTTP requests
* PostgreSQL
* Redis
* file storage
* task queues
* external services

---

## External Systems

The application communicates with:

* Public job APIs
* RSS feeds
* PostgreSQL
* Redis
* Other external services

---

# 📂 Project Structure

The final project is expected to follow a structure similar to:

```text
job-aggregator/
│
├── app/
│   │
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── jobs.py
│   │   │   ├── users.py
│   │   │   ├── searches.py
│   │   │   └── recommendations.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── cli/
│   │   └── commands/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── domain/
│   │   ├── models/
│   │   └── schemas/
│   │
│   ├── sources/
│   │   ├── base.py
│   │   ├── source_a.py
│   │   ├── source_b.py
│   │   └── rss.py
│   │
│   ├── services/
│   │   ├── aggregation.py
│   │   ├── job_service.py
│   │   ├── search_service.py
│   │   └── recommendation_service.py
│   │
│   ├── processors/
│   │   ├── normalizer.py
│   │   ├── deduplicator.py
│   │   ├── tagger.py
│   │   └── ranking.py
│   │
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks/
│   │       ├── aggregation.py
│   │       ├── processing.py
│   │       └── recommendations.py
│   │
│   ├── ml/
│   │   ├── datasets/
│   │   ├── preprocessing/
│   │   ├── models/
│   │   ├── training/
│   │   └── inference/
│   │
│   ├── repositories/
│   │   ├── jobs.py
│   │   ├── users.py
│   │   └── sources.py
│   │
│   └── exporters/
│       ├── csv.py
│       └── json.py
│
├── tests/
│
├── migrations/
│
├── data/
│
├── output/
│
├── docker/
│
├── main.py
├── worker.py
├── pyproject.toml
├── docker-compose.yml
└── README.md
```

> This represents the intended final architecture. Not every directory or component will exist during the early stages of development.

---

# 🔄 Data Pipeline

The core aggregation pipeline is:

```text
                Job Sources
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      API A       API B       RSS C
        │           │           │
        └───────────┼───────────┘
                    ▼
          Concurrent Fetching
                    │
                    ▼
              Raw Job Data
                    │
                    ▼
              Normalization
                    │
                    ▼
              Deduplication
                    │
                    ▼
              Keyword Tagging
                    │
                    ▼
               ML Ranking
                    │
                    ▼
                PostgreSQL
                    │
             ┌──────┴──────┐
             ▼             ▼
          REST API        CLI
             │
             ▼
        React Frontend
```

---

# 🌐 Job Sources

The system is designed around a source abstraction.

Every source is responsible for retrieving and translating external data into the application's internal `Job` representation.

Conceptually:

```text
External API
     ↓
Source Adapter
     ↓
Job
```

This means the rest of the application doesn't need to know how a particular API represents its jobs.

For example:

```text
Source A
    ↓
┌──────────────┐
│ external JSON│
└──────┬───────┘
       ↓
     Job
```

and:

```text
RSS Source
    ↓
┌──────────────┐
│ XML / RSS    │
└──────┬───────┘
       ↓
     Job
```

Both eventually produce the same internal representation.

---

# ⚡ Concurrent Fetching

Job sources are primarily network-bound.

Waiting for one source before contacting another would unnecessarily increase execution time.

Therefore, the initial implementation will use Python's:

```text
concurrent.futures
```

with a thread pool.

Conceptually:

```text
                 Aggregator
                     │
             Concurrent Fetcher
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Source A   Source B   Source C
          │          │          │
          └──────────┼──────────┘
                     ▼
                 Job Results
```

The concurrency layer will handle:

* worker management
* futures
* timeouts
* exceptions
* result collection

The project may later experiment with `asyncio` to compare asynchronous I/O with thread-based concurrency.

---

# 🧹 Data Normalization

Different sources may represent the same information differently.

For example:

```text
" PYTHON Developer "
"Python developer"
"python DEVELOPER"
```

The normalization layer converts inconsistent data into a consistent format.

Normalization may include:

* whitespace normalization
* capitalization
* URL normalization
* date parsing
* location normalization
* company-name normalization
* missing-value handling
* description cleanup

---

# 🔍 Deduplication

The application will use multiple levels of duplicate detection.

## Exact duplicates

Possible identifiers:

```text
source + external_job_id
```

or:

```text
URL
```

## Structured duplicates

Potential comparison of:

```text
company
+
title
+
location
```

## Near duplicates

More advanced processing may compare job text using:

* token similarity
* TF-IDF
* cosine similarity
* other NLP techniques

The goal is to prevent the same job from appearing multiple times in the final results.

---

# 🏷️ Job Tagging

Jobs will be categorized based on their content.

Example taxonomy:

```text
Languages
├── Python
├── PHP
├── JavaScript
└── Java

Frameworks
├── Laravel
├── React
├── Vue
└── FastAPI

Technologies
├── Docker
├── AWS
├── PostgreSQL
└── Redis

Roles
├── Frontend
├── Backend
├── Full Stack
├── DevOps
└── Machine Learning
```

A single job can have multiple tags.

Example:

```text
Senior Full Stack Developer

Tags:
- Python
- FastAPI
- React
- PostgreSQL
- Backend
- Frontend
- Full Stack
```

The initial implementation will use keyword-based rules.

Later, ML/NLP methods may improve classification.

---

# 🤖 Machine Learning

Machine learning is intentionally introduced after the traditional aggregation pipeline is functional.

The ML component will evolve through several stages.

## Stage 1 — Similarity

Use TF-IDF to represent job descriptions numerically.

```text
Job description
       ↓
     TF-IDF
       ↓
   Vector
```

A user profile can also be represented as a vector.

```text
User profile
       ↓
     TF-IDF
       ↓
   Vector
```

The vectors can then be compared using cosine similarity.

```text
User profile
     │
     │ cosine similarity
     ▼
    Jobs
     │
     ▼
Relevance score
```

---

## Stage 2 — Supervised Classification

The application can collect user feedback:

```text
Relevant
Not relevant
```

This produces a training dataset.

Possible initial models include:

* Logistic Regression
* Linear SVM

The model will predict the probability or classification of a job being relevant to a user.

---

## Stage 3 — Semantic Embeddings

Later, the project can experiment with sentence/document embeddings.

Instead of relying only on exact words, embeddings allow the system to capture semantic relationships between job descriptions and user preferences.

Conceptually:

```text
Job
 ↓
Embedding model
 ↓
Vector
```

and:

```text
User profile
 ↓
Embedding model
 ↓
Vector
```

The vectors can then be compared to determine semantic similarity.

---

## Stage 4 — Personalized Recommendations

The final recommendation system may combine:

```text
User skills
+
Search history
+
Saved jobs
+
Viewed jobs
+
Explicit feedback
+
Job tags
+
Semantic similarity
+
ML predictions
```

to produce a personalized ranking.

Example:

```text
Python Backend Engineer      94%
FastAPI Developer             91%
Laravel Backend Developer     83%
React Developer               61%
Graphic Designer               8%
```

The recommendation system should remain modular so that different ranking strategies can be tested.

---

# 👤 User Personalization

Once the frontend and authentication system exist, users can have profiles containing:

* skills
* technologies
* preferred locations
* preferred job types
* saved jobs
* search history
* job interactions
* recommendation feedback

The system can use this information to improve future recommendations.

---

# 🗄️ Database

During the initial CLI stage, results can be exported to CSV.

As the project evolves, PostgreSQL becomes the primary persistent storage.

Potential entities include:

```text
users
companies
sources
jobs
tags
job_tags
user_profiles
user_preferences
saved_jobs
job_interactions
recommendations
model_versions
```

CSV and JSON remain useful as export formats.

---

# 🔄 Background Processing

Once the system becomes a web application, job aggregation should not happen during a user's HTTP request.

Instead:

```text
Scheduler
    ↓
Task Queue
    ↓
Worker
    ↓
Job Sources
    ↓
Processing
    ↓
PostgreSQL
```

Redis will be used as the message broker/cache and Celery will manage background tasks.

Possible background tasks:

* Fetch jobs
* Process jobs
* Deduplicate jobs
* Generate embeddings
* Update recommendations
* Clean expired jobs
* Generate reports

---

# ⏰ Scheduled Aggregation

The system should periodically retrieve new jobs automatically.

Conceptually:

```text
Scheduler
    │
    ├── Every N hours
    │
    ▼
Aggregation Task
    │
    ▼
Workers
    │
    ▼
Job Sources
    │
    ▼
Database
```

This allows the frontend to serve already-processed job listings instead of waiting for external sources.

---

# 🚀 REST API

FastAPI will expose the application's functionality to the frontend and other clients.

Potential endpoints:

```text
GET    /jobs
GET    /jobs/{id}

GET    /search
GET    /sources
GET    /tags

POST   /auth/register
POST   /auth/login

GET    /me
GET    /me/saved-jobs
POST   /me/saved-jobs

GET    /recommendations
```

The API will be responsible for:

* validation
* authentication
* authorization
* pagination
* filtering
* error handling
* rate limiting
* exposing application services

---

# 🖥️ Frontend

The planned frontend will use:

* React
* Tailwind CSS

Potential pages:

```text
Home
Search
Job Details
Saved Jobs
Profile
Recommendations
```

The frontend will communicate exclusively with the application's API rather than directly with job-board APIs.

```text
React
   │
   ▼
FastAPI
   │
   ▼
Application Services
```

This keeps API credentials, aggregation logic, and business logic on the server.

---

# 🛡️ Security

The production version will consider:

* authentication
* authorization
* password hashing
* secure session/token handling
* input validation
* CORS
* rate limiting
* SQL injection prevention
* XSS prevention
* CSRF considerations where applicable
* secure secret management
* HTTPS
* secure HTTP headers

Secrets and API credentials will never be committed to the repository.

---

# 📊 Observability

The production version should provide visibility into system behavior.

Examples:

```text
Jobs fetched
Jobs processed
Duplicates removed
Source failures
API response time
Worker failures
Queue size
Database performance
Recommendation requests
```

The system will use structured logging and may later integrate external monitoring/error-tracking services.

---

# 🧪 Testing

Testing will be introduced throughout development instead of being postponed until the end.

## Unit tests

Individual components:

```text
Normalizer
Deduplicator
Tagger
Ranker
Repository
```

## Integration tests

Interactions between:

```text
FastAPI
PostgreSQL
Redis
Workers
```

## End-to-end tests

Testing complete workflows:

```text
Frontend
   ↓
API
   ↓
Database
   ↓
Background worker
   ↓
Job source
```

External job APIs should be mocked during most tests so that tests are deterministic and don't depend on third-party availability.

---

# 🐳 Containerization

The final development/production environment is expected to use Docker.

Potential services:

```text
frontend
backend
worker
scheduler
postgres
redis
```

Docker Compose can be used for local development.

The deployment architecture may eventually look like:

```text
                 Reverse Proxy
                      │
              ┌───────┴───────┐
              ▼               ▼
          Frontend          FastAPI
                               │
                    ┌──────────┼──────────┐
                    ▼          ▼          ▼
                PostgreSQL   Redis      Workers
```

---

# 🔁 CI/CD

The project will eventually use automated CI/CD.

Expected pipeline:

```text
git push
   ↓
CI
   ↓
Lint
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
Build
   ↓
Docker Image
   ↓
Deployment
```

The goal is to make deployments repeatable and reduce the possibility of introducing broken code into production.

---

# 📈 Development Roadmap

## Phase 1 — Foundation

* Python project setup
* Git repository
* Virtual environment
* Package structure
* Configuration
* Logging

## Phase 2 — Domain

* Job model
* Company model
* Source model
* Tags
* Type hints
* Validation

## Phase 3 — Sources

* Source abstraction
* First API
* Second API
* RSS source
* Error handling
* Retries
* Timeouts

## Phase 4 — Concurrency

* ThreadPoolExecutor
* Futures
* Concurrent source fetching
* Timeout handling
* Worker errors

## Phase 5 — Processing

* Normalization
* Exact deduplication
* Near-duplicate detection
* Keyword tagging
* Filtering
* Sorting

## Phase 6 — CLI

* Fetch command
* Search command
* Export command
* Source management
* Filtering options

## Phase 7 — Persistence

* PostgreSQL
* SQLAlchemy
* Migrations
* Repository layer

## Phase 8 — Background Processing

* Redis
* Celery
* Workers
* Scheduled aggregation
* Retry policies

## Phase 9 — API

* FastAPI
* REST endpoints
* Validation
* Authentication
* Authorization
* Pagination

## Phase 10 — Frontend

* React
* Tailwind CSS
* Authentication UI
* Search
* Job details
* Saved jobs
* User profile

## Phase 11 — Machine Learning

* TF-IDF
* Cosine similarity
* Dataset creation
* User feedback
* Classification
* Evaluation
* Embeddings
* Personalized ranking

## Phase 12 — Production

* Automated tests
* Docker
* CI/CD
* HTTPS
* Logging
* Monitoring
* Security hardening
* Deployment

---

# 🧠 Educational Objectives

This project is intentionally designed to cover multiple areas of software engineering.

### Python

* OOP
* type hints
* decorators
* context managers
* exceptions
* concurrency
* asynchronous programming
* package architecture

### Networking

* HTTP
* REST APIs
* RSS
* timeouts
* retries
* rate limits

### Databases

* PostgreSQL
* SQL
* ORM
* indexes
* relationships
* migrations

### Backend

* FastAPI
* REST architecture
* authentication
* validation
* background processing

### Distributed processing

* Redis
* Celery
* queues
* workers
* scheduled jobs

### Machine Learning

* NLP
* TF-IDF
* vectorization
* similarity
* classification
* embeddings
* recommendation systems
* model evaluation

### DevOps

* Docker
* CI/CD
* reverse proxies
* deployment
* monitoring
* logging

### Frontend

* React
* Tailwind CSS
* API integration
* state management
* authentication
* responsive UI

---

# 🧩 Design Principles

The project follows several principles throughout development.

### Separation of concerns

Each component should have a clearly defined responsibility.

### Dependency inversion

Core application logic should not depend directly on external APIs or infrastructure.

### Source abstraction

Adding a new job source should require minimal changes to the rest of the application.

### Replaceable components

The following should be replaceable independently:

```text
Job Source
Database
Queue
Ranking Algorithm
ML Model
Exporter
Frontend
```

### Progressive complexity

Complex infrastructure should only be introduced when it solves an actual problem.

### Testability

Components should be designed so they can be tested independently.

### Security by design

Security should be considered throughout development rather than added immediately before deployment.

---

# 📦 Technology Stack

## Current / Planned

| Layer          | Technology          |
| -------------- | ------------------- |
| Language       | Python              |
| CLI            | Typer               |
| HTTP Client    | HTTPX               |
| API            | FastAPI             |
| Validation     | Pydantic            |
| ORM            | SQLAlchemy          |
| Database       | PostgreSQL          |
| Queue          | Celery              |
| Cache / Broker | Redis               |
| ML             | scikit-learn        |
| NLP            | TF-IDF / embeddings |
| Frontend       | React               |
| Styling        | Tailwind CSS        |
| Testing        | pytest              |
| Containers     | Docker              |
| Reverse Proxy  | Nginx / Caddy       |
| CI/CD          | GitHub Actions      |

Technologies may change during development when a different solution provides a better learning opportunity or technical fit.

---

# 🚦 Initial MVP

The first usable version will intentionally be much smaller than the final platform.

```text
3 Job Sources
      ↓
Concurrent Fetching
      ↓
Normalization
      ↓
Deduplication
      ↓
Keyword Tagging
      ↓
CSV Export
```

The MVP should be reliable before additional infrastructure is introduced.

---

# 🔮 Long-Term Vision

The final application aims to become a personal intelligent job-search platform.

A user should be able to:

```text
1. Create an account
2. Define their skills and preferences
3. Search thousands of aggregated jobs
4. Filter jobs by technology/location/etc.
5. Save interesting jobs
6. Receive personalized recommendations
7. Give feedback on recommendations
8. Improve future recommendations through that feedback
```

The system will continuously collect and process job listings in the background.

```text
             Job Sources
                  │
                  ▼
            Aggregation
                  │
                  ▼
             Processing
                  │
                  ▼
             PostgreSQL
                  │
                  ▼
         Recommendation Engine
                  │
                  ▼
                User
                  │
                  ▼
             Feedback
                  │
                  └──────────────► Model
```

The ultimate goal is not simply to aggregate jobs, but to build a system that **learns which opportunities are most relevant to each user**.

---

# ⚖️ Data & Source Considerations

The application should only use job sources in ways permitted by their APIs, RSS feeds, terms of service, robots policies, and applicable laws.

Where possible, official public APIs and RSS feeds should be preferred over scraping.

Source adapters should also respect:

* API rate limits
* request limits
* attribution requirements
* terms of service
* robots policies where applicable
* source-specific data restrictions

The system is intended for legitimate job-search and educational purposes.

---

# 📄 License

License information will be added once the project's distribution model is finalized.

---

# 👨‍💻 Development Philosophy

This project is being built progressively.

The objective is not to immediately assemble a large collection of frameworks.

Instead:

```text
Simple
  ↓
Correct
  ↓
Tested
  ↓
Modular
  ↓
Concurrent
  ↓
Persistent
  ↓
Distributed
  ↓
Intelligent
  ↓
Production-ready
```

Every major technology should solve a real problem in the system and provide an opportunity to understand the underlying engineering concept.

---

## ⭐ Final Goal

Build a complete, production-oriented job platform that combines:

**Python + concurrency + APIs + PostgreSQL + Redis + background workers + FastAPI + React + NLP + machine learning + Docker + CI/CD**

while maintaining a clean architecture that can evolve without requiring the entire system to be rewritten.
