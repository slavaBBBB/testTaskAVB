from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
import hashlib
import uvicorn

app = FastAPI()

url_storage = {}

@app.post("/")
async def short_link(
    request: Request
):
    url = (await request.body()).decode("utf-8")

    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    url_storage[url_hash] = url

    return JSONResponse(
        {"short_url": f"http://127.0.0.1:8080/{url_hash}"},
        status_code=201
    )

@app.get("/{url_hash}")
async def redirect_to_orig(
    url_hash: str
):
    if url_hash not in url_storage:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url_storage[url_hash], status_code=307)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)