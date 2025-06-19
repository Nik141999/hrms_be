from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, user_route, roles_route, leave_route, org_route, department_route, time_tracker_route, org_type_route

app = FastAPI(
    title="HRMS BACKEND APPLICATION",
    version="v0", 
    description="A template for FastAPI projects",
)


origins = [
    "http://localhost",
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your routers
app.include_router(auth.router)
app.include_router(org_route.router)
app.include_router(user_route.router)
app.include_router(roles_route.router)
app.include_router(leave_route.router)
app.include_router(department_route.router)
app.include_router(time_tracker_route.router)
app.include_router(org_type_route.router)
@app.get("/", tags=["health"])
async def health():
    return {"message": "Hello World"}
