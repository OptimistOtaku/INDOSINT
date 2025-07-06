from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    search,
    osint,
    analysis,
    reports,
    face_recognition,
    digital_dna,
    visualization,
    data_sources,
    system
)

api_router = APIRouter()

# Authentication and user management
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Core OSINT functionality
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(osint.router, prefix="/osint", tags=["osint"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])

# Advanced features
api_router.include_router(face_recognition.router, prefix="/face-recognition", tags=["face-recognition"])
api_router.include_router(digital_dna.router, prefix="/digital-dna", tags=["digital-dna"])
api_router.include_router(visualization.router, prefix="/visualization", tags=["visualization"])

# Reports and data management
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(data_sources.router, prefix="/data-sources", tags=["data-sources"])

# System management
api_router.include_router(system.router, prefix="/system", tags=["system"]) 