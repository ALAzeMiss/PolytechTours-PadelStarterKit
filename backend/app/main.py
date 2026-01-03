from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api import auth, user, match, player
from app.database import engine
from app.models import models

# Créer les tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Corpo Padel API",
    description="API pour la gestion de tournois corporatifs de padel",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de sécurité
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Gestionnaire d'erreurs personnalisé pour traduire les messages en français
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Traduire les messages d'erreur courants en français
    french_messages = {
        404: "Ressource introuvable",
        403: "Accès refusé",
        401: "Non autorisé",
        400: "Requête invalide",
        500: "Erreur interne du serveur"
    }
    
    # Utiliser le message de l'exception s'il existe, sinon utiliser le message traduit
    detail = exc.detail
    if exc.detail == "Not Found":
        detail = french_messages.get(exc.status_code, exc.detail)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": detail}
    )

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Creation Users"])
app.include_router(match.router, prefix="/api/v1/matches", tags=["Creation Matches"])
app.include_router(player.router, prefix="/api/v1/players", tags=["players"])


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Corpo Padel", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}