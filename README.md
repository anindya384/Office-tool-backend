# MyOfficePal Rembg Backend

This is a standalone backend service for AI-powered background removal, designed for integration with the MyOfficePal frontend.

## Features
- High-quality background removal using [rembg](https://github.com/danielgatis/rembg)
- Batch processing support
- Background replacement (solid color, texture, or preset image)
- REST API (FastAPI)
- CORS enabled for frontend integration

## Requirements
- Python 3.8+
- pip

## Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Server
```bash
uvicorn main:app --reload
```

## API Endpoints
### POST `/remove-bg`
- Accepts: Multipart form-data with one or more images
- Optional: Background replacement options (color, texture, preset)
- Returns: Processed images (PNG with transparency or replaced background)

## Example Request (cURL)
```bash
curl -X POST "http://localhost:8000/remove-bg" \
  -F "images=@/path/to/image1.jpg" \
  -F "images=@/path/to/image2.png" \
  -F "bg_color=#ffffff" # Optional
```

## Notes
- For best results, use high-quality images.
- Textures/preset backgrounds can be added to the `backgrounds/` folder.

---
MIT License 