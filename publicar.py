import markdown

import os
from datetime import datetime


def generar_nota(ruta_md, nombre_salida):
    if not os.path.exists(ruta_md):
        print(f"❌ Error: No existe {ruta_md}")
        return

    with open(ruta_md, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    if len(lineas) < 4:
        print("❌ Error: El archivo .md no tiene el formato correcto (4 líneas mínimo)")
        return

    titulo, imagen, descripcion, seccion = (
        lineas[0],
        lineas[1],
        lineas[2],
        lineas[3].lower(),
    )
    cuerpo_md = "\n\n".join(lineas[4:])
    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazo de etiquetas para el diseño sin barra lateral
    final = (
        plantilla.replace("{{TITULO}}", titulo)
        .replace("{{IMAGEN}}", imagen)
        .replace("{{DESCRIPCION}}", descripcion)
        .replace("{{CONTENIDO}}", contenido_html)
    )

    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"✅ Nota creada exitosamente: {nombre_salida}")


if __name__ == "__main__":
    print("\n--- GENERADOR DE NOTA INDIVIDUAL ---")
    archivo_md = input("Introduce el nombre del .md (ej: nota2.md): ")
    ruta_completa = os.path.join("content", "codigorojo", archivo_md)

    # Generar nombre con fecha automática
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    contador = 1
    nombre_final = f"{fecha_hoy}-{contador:02d}.html"

    # Evitar sobrescribir archivos del mismo día
    while os.path.exists(nombre_final):
        contador += 1
        nombre_final = f"{fecha_hoy}-{contador:02d}.html"

    generar_nota(ruta_completa, nombre_final)
