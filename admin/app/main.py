from fastapi import FastAPI
from app.api.routes.admin_user import router as admin_router
from app.api.routes.users import router as enrolled_users_router
from app.api.routes.books import router as books_router

# Create the FastAPI app instance
app = FastAPI()


# Include the dynamic admin user router into the main app
app.include_router(admin_router, prefix="/admin", tags=["Admin & Super Users"])

# Include the user router into the main app
app.include_router(enrolled_users_router, prefix="/admin/users", tags=["Enrolled Users"])

# Include the book router into the main app
app.include_router(books_router, prefix="/admin/books", tags=["Books"])



# create an API to check reachability of the general API
@app.get("/admin/health-check", tags=["Health-Status"])
def home():
    return {"Backend APIs is reachable. This is just a Health Check"}