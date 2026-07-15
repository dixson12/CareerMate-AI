from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload
from app.routers import upload, chat

# ...after app = FastAPI(...) and CORS middleware...





app = FastAPI(title=settings.app_name)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(upload.router)
# Allow Streamlit (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in Sprint 5 for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}