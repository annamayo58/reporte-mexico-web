import markdown
import sys
import os


def generar_nota(ruta_archivo_md):
    if not os.path.exists(ruta_archivo_md):
        print(f"❌ Error: No se encontró el archivo en {ruta_archivo_md}")
        return

    with open(ruta_archivo_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Validar que la nota tenga el contenido mínimo necesario
    if len(lineas) < 4:
        print(f"⚠️ Nota incompleta: {ruta_archivo_md}")
        return

    titulo = lineas[0].strip().replace("# ", "")
    imagen = lineas[1].strip()
    descripcion = lineas[2].strip()
    seccion = lineas[3].strip().lower()
    cuerpo_md = "".join(lineas[4:])

    # Diccionario unificado al estilo Púrpura de Reporte México
    colores_nav = {
        "codigo-rojo": "bg-red-600",
        "default": "bg-purple-600",  # Color base para todas las demás secciones
    }

    color_final = colores_nav.get(seccion, colores_nav["default"])
    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    final = plantilla.replace("{{CONTENIDO}}", contenido_html)
    final = final.replace("{{TITULO}}", titulo)
    final = final.replace("{{IMAGEN}}", imagen)
    final = final.replace("{{DESCRIPCION}}", descripcion)
    final = final.replace("{{NAV_COLOR}}", color_final)

    nombre_base = os.path.basename(ruta_archivo_md).replace(".md", "")
    final = final.replace("{{ARCHIVO}}", nombre_base)

    nombre_salida = nombre_base + ".html"
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)

    print(f"✅ Generada: {nombre_salida}")


if __name__ == "__main__":
    # Si pasas un archivo por terminal (ej: python publicar.py content/tijuana/nota.md)
    if len(sys.argv) > 1:
        generar_nota(sys.argv[1])
    else:
        # BARRIDO AUTOMÁTICO DE TODAS LAS CARPETAS
        print("🚀 Iniciando barrido de todas las carpetas...")
        carpetas = [
            "codigorojo",
            "tijuana",
            "bajacalifornia",
            "rosarito",
            "tecate",
            "desaparecidos",
            "empleos",
        ]

        for carpeta in carpetas:
            ruta_busqueda = os.path.join("content", carpeta)
            if os.path.exists(ruta_busqueda):
                for archivo in os.listdir(ruta_busqueda):
                    if archivo.endswith(".md"):
                        generar_nota(os.path.join(ruta_busqueda, archivo))


def generar_portadas(carpetas):
    todas_las_notas = []

    for carpeta in carpetas:
        ruta = os.path.join("content", carpeta)
        if not os.path.exists(ruta):
            continue

        for archivo in os.listdir(ruta):
            if archivo.endswith(".md"):
                with open(os.path.join(ruta, archivo), "r", encoding="utf-8") as f:
                    lineas = f.readlines()
                    if len(lineas) < 4:
                        continue

                    nota = {
                        "titulo": lineas[0].strip().replace("# ", ""),
                        "imagen": lineas[1].strip(),
                        "resumen": lineas[2].strip(),
                        "url": archivo.replace(".md", ".html"),
                        "seccion": carpeta,
                    }
                    todas_las_notas.append(nota)

    # Crear el HTML de las tarjetas
    html_tarjetas = ""
    for nota in todas_las_notas:
        html_tarjetas += f"""
        <div class="bg-slate-800 rounded-lg overflow-hidden shadow-lg hover:scale-105 transition-transform">
            <img src="static/images/{nota['imagen']}" class="w-full h-48 object-cover">
            <div class="p-4">
                <span class="text-purple-400 text-xs font-bold uppercase">{nota['seccion']}</span>
                <h3 class="text-white font-bold text-xl mt-1">{nota['titulo']}</h3>
                <p class="text-slate-400 text-sm mt-2">{nota['resumen']}</p>
                <a href="{nota['url']}" class="inline-block mt-4 text-purple-400 font-bold hover:underline">Leer más →</a>
            </div>
        </div>
        """

    # Guardar en index.html usando una plantilla de portada
    with open("template_portada.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(plantilla.replace("{{TARJETAS}}", html_tarjetas))

    print("🏠 Portada principal (index.html) actualizada.")

    # Dentro de tu función generar_nota:


imagen = lineas[1].strip()
if not imagen or imagen.lower() == "ninguna":
    imagen = "logo-social.png"  # Tu logo púrpura cuadrado para redes
