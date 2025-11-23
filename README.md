# rest-api
# FastAPI + Angular 21 Full-Stack Application

This project is a **full-stack application** that provides restaurant search functionality powered by the Yelp API.

- **Frontend:** Angular 21 application  
- **Backend:** Python FastAPI REST API  
- **Cache:** Redis (for caching restaurant search results)  
- **Containerization:** Docker & Docker Compose  

---

## Prerequisites

- **Docker Desktop**  
- **Docker Compose**  
- Optional for local (non-Docker) development:
  - **Python 3.11+**
  - **FastAPI** + **Uvicorn**
  - **Node.js LTS**
  - **Angular CLI 19+**

---

## Project Structure

```text
/project-root
├─ /api                 # FastAPI backend
│  ├─ Dockerfile
│  ├─ services/
│  ├─ models/
│  ├─ config/
│  ├─ common/
│  ├─ .env
│  └─ ...
├─ /webApp              # Angular frontend
│  ├─ Dockerfile
│  ├─ src/
│  └─ ...
├─ docker-compose.yml
└─ README.md
```
---

## Docker Compose

The included **docker-compose.yml** file defines three services:

- **api** – FastAPI backend  
- **ui** – Angular 21 frontend  
- **redis** – In-memory cache used by the API  

### Docker Compose will:

- Build the **FastAPI backend** using `/api/Dockerfile`
- Build the **Angular frontend** using `/webApp/Dockerfile`
- Start **Redis** for caching API results
- Create a shared **app-network** for container communication
- Mount your local code into the containers for live development
- Expose ports:
  - **8000** → FastAPI
  - **4200** → Angular
  - **6379** → Redis

---

## Running the App with Docker Compose
### From the project root:
```bash 
docker compose up 
```

## Access the Application

| Service              | URL                        |
|---------------------|----------------------------|
| Angular Frontend     | http://localhost:4200      |
| FastAPI Backend      | http://localhost:8000      |
| API Docs (Swagger)   | http://localhost:8000/docs |
| Redis                | localhost:6379             |

## Shutting down the App with Docker Compose
### From the project root:
```bash 
docker compose down
```
## Running unit tests
```bash 
 PYTHONPATH=. pytest -v tests  
 ```