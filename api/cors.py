from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """
    Adds CORS middleware to the given FastAPI app.
    """
    origins = [
        "http://localhost:4200",  # Angular dev server
        "http://127.0.0.1:4200",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )