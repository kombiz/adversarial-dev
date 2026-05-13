from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"status": "error"},
    )
