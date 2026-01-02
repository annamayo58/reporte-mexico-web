import markdown
import sys
import os


def generar_nota(ruta_archivo_md):
    # Verificamos si el archivo existe en la ruta proporcionada
    if not os.path.exists(ruta_archivo_md):
        print(f"❌ Error: No se encontró el archivo en {ruta_archivo_md}")
        return

    with open(ruta_archivo_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Extraemos metadatos (Título, Imagen, Descripción, Sección)
    titulo = lineas[0].strip().replace("# ", "")
    imagen = lineas[1].strip()
    descripcion = lineas[2].strip()
    seccion = lineas[3].strip().lower()
    cuerpo_md = "".join(lineas[4:])

    # Diccionario de colores para la barra de navegación
    colores_nav = {
        "codigo-rojo": "bg-red-900",
        "desaparecidos": "bg-slate-800",
        "tijuana": "bg-blue-900",
        "default": "bg-slate-900",
    }

    color_final = colores_nav.get(seccion, colores_nav["default"])
    contenido_html = markdown.markdown(cuerpo_md)

    # Cargamos la plantilla
    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazos en la plantilla
    final = plantilla.replace("{{CONTENIDO}}", contenido_html)
    final = final.replace("{{TITULO}}", titulo)
    final = final.replace("{{IMAGEN}}", imagen)
    final = final.replace("{{DESCRIPCION}}", descripcion)
    final = final.replace("{{NAV_COLOR}}", color_final)

    # Extraemos solo el nombre del archivo (sin carpetas) para el enlace
    nombre_base = os.path.basename(ruta_archivo_md).replace(".md", "")
    final = final.replace("{{ARCHIVO}}", nombre_base)

    # Guardamos el HTML resultante SIEMPRE en la carpeta raíz
    nombre_salida = nombre_base + ".html"
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"✅ Nota generada con éxito en la raíz: {nombre_salida}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        generar_nota(sys.argv[1])
