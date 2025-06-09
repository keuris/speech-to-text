from fastapi import FastAPI, File, UploadFile
import whisper
import shutil
import os
import uuid

app = FastAPI()

# Cargar el modelo una vez
model = whisper.load_model("base")

@app.post("/transcribir/")
async def transcribir_audio(file: UploadFile = File(...)):
    # Crear un nombre único para el archivo temporal
    temp_filename = f"temp_{uuid.uuid4()}.mp3"
    
    # Guardar el archivo recibido
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Transcribir el audio
        result = model.transcribe(temp_filename)
        texto = result["text"]
    finally:
        # Eliminar archivo temporal
        os.remove(temp_filename)

    return {"transcripcion": texto}
