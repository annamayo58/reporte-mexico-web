import markdown
import os


def generar_nota(archivo_md):
    with open(archivo_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Extraemos metadatos sencillos de las primeras líneas del archivo .md
    # Ejemplo: primera línea es el título, segunda la imagen, tercera la descripción
    titulo = lineas[0].strip().replace("# ", "")
    imagen = lineas[1].strip()
    descripcion = lineas[2].strip()
    cuerpo_md = "".join(lineas[3:])

    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazo de etiquetas
    final = plantilla.replace("{{CONTENIDO}}", contenido_html)
    final = final.replace("{{TITULO}}", titulo)
    final = final.replace("{{IMAGEN}}", imagen)
    final = final.replace("{{DESCRIPCION}}", descripcion)
    final = final.replace("{{ARCHIVO}}", archivo_md.replace(".md", ""))

    nombre_salida = archivo_md.replace(".md", ".html")
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"✅ Nota lista con etiquetas de Facebook: {nombre_salida}")


if __name__ == "__main__":
    import sys

    generar_nota(sys.argv[1])
