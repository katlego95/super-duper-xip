import os

import strawberry
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="PaySense API",
    description="AI-powered group finance platform",
    version="0.1.0",
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define basic GraphQL schema
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Welcome to PaySense API!"


@strawberry.type
class Mutation:
    @strawberry.field
    def placeholder(self) -> str:
        return "Mutations coming soon"


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Mount GraphQL
app.include_router(graphql_app, prefix="/graphql")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "paysense-backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
