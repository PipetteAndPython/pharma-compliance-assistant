from pypdf import PdfReader  # Librería que permite abrir PDFs y extraer texto
from pathlib import Path     # Manejo moderno de rutas (evita problemas con \ en Windows)

def load_pdfs(folder_path):
    # Convertimos la ruta en un objeto Path (más robusto que string)
    folder = Path(folder_path)

    # Aquí vamos a guardar todos los documentos leídos
    docs = []

    # Recorre todos los archivos que terminen en .pdf dentro de la carpeta
    for pdf_file in folder.glob("*.pdf"):

        # Abre el PDF
        reader = PdfReader(pdf_file)

        # Variable donde juntamos todo el texto del PDF
        text = ""

        # Recorremos cada página del PDF
        for page in reader.pages:

            # Extrae el texto de la página
            # (puede devolver None si la página es escaneada o imagen)
            text += page.extract_text() or ""

        # Guardamos el resultado en una estructura tipo diccionario
        docs.append({
            "file": pdf_file.name,  # nombre del archivo
            "text": text            # contenido completo del PDF
        })

    # Devuelve todos los PDFs ya convertidos a texto
    return docs