from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Optional
from io import BytesIO
from rembg import remove
from PIL import Image, ImageColor
import os

app = FastAPI()

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for preset backgrounds/textures
BG_DIR = os.path.join(os.path.dirname(__file__), "backgrounds")

@app.post("/remove-bg")
async def remove_bg(
    images: List[UploadFile] = File(...),
    bg_color: Optional[str] = Form(None),
    bg_texture: Optional[str] = Form(None),
    bg_preset: Optional[str] = Form(None)
):
    results = []
    for image_file in images:
        input_bytes = await image_file.read()
        input_image = Image.open(BytesIO(input_bytes)).convert("RGBA")
        # Remove background
        output_image = remove(input_image)
        # Background replacement
        if bg_color:
            try:
                color = ImageColor.getrgb(bg_color)
                bg = Image.new("RGBA", output_image.size, color + (255,))
                output_image = Image.alpha_composite(bg, output_image)
            except Exception:
                pass
        elif bg_texture:
            texture_path = os.path.join(BG_DIR, bg_texture)
            if os.path.exists(texture_path):
                texture = Image.open(texture_path).convert("RGBA").resize(output_image.size)
                output_image = Image.alpha_composite(texture, output_image)
        elif bg_preset:
            preset_path = os.path.join(BG_DIR, bg_preset)
            if os.path.exists(preset_path):
                preset = Image.open(preset_path).convert("RGBA").resize(output_image.size)
                output_image = Image.alpha_composite(preset, output_image)
        # Save to bytes
        buf = BytesIO()
        output_image.save(buf, format="PNG")
        buf.seek(0)
        results.append((image_file.filename, buf.read()))
    # If one image, return as image; if many, return as JSON with base64 or as zip (future)
    if len(results) == 1:
        filename, data = results[0]
        return StreamingResponse(BytesIO(data), media_type="image/png", headers={"Content-Disposition": f"attachment; filename=removed-{filename}.png"})
    else:
        # For now, return JSON with base64 (for demo); can switch to zip for production
        import base64
        return JSONResponse([
            {"filename": f"removed-{fn}.png", "data": base64.b64encode(d).decode()} for fn, d in results
        ]) 