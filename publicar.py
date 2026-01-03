import markdown
import sys
import os


def generar_nota(ruta_archivo_md):
    if not os.path.exists(ruta_archivo_md):
        print(f"❌ Error: No se encontró {ruta_archivo_md}")
        return

    with open(ruta_archivo_md, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    if len(lineas) < 4:
        return

    titulo = lineas[0].strip().replace("# ", "")
    imagen = lineas[1].strip()
    descripcion = lineas[2].strip()
    seccion = lineas[3].strip().lower()
    cuerpo_md = "".join(lineas[4:])

    # Si la línea de imagen está vacía, usamos el logo por defecto
    if not imagen or imagen.lower() == "ninguna":
        imagen = "logo-social.webp"

    colores_nav = {"codigo-rojo": "bg-red-600", "default": "bg-purple-600"}
    color_final = colores_nav.get(seccion, colores_nav["default"])
    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    final = plantilla.replace("{{CONTENIDO}}", contenido_html).replace(
        "{{TITULO}}", titulo
    )
    final = final.replace("{{IMAGEN}}", imagen).replace("{{DESCRIPCION}}", descripcion)
    final = final.replace("{{NAV_COLOR}}", color_final)

    nombre_base = os.path.basename(ruta_archivo_md).replace(".md", "")
    nombre_salida = nombre_base + ".html"

    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)
    print(f"✅ Nota: {nombre_salida}")


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
                    if len(lineas) < 3:
                        continue
                    img_nota = lineas[1].strip()
                    if not img_nota or img_nota.lower() == "ninguna":
                        img_nota = "logo-social.webp"

                    todas_las_notas.append(
                        {
                            "titulo": lineas[0].strip().replace("# ", ""),
                            "imagen": img_nota,
                            "resumen": lineas[2].strip(),
                            "url": archivo.replace(".md", ".html"),
                            "seccion": carpeta,
                        }
                    )

    html_tarjetas = ""
    for nota in todas_las_notas:
        html_tarjetas += f"""
        <div class="bg-slate-800 rounded-lg overflow-hidden shadow-lg hover:scale-105 transition-transform border border-slate-700">
            <div class="w-full h-48 bg-[#111827] flex items-center justify-center overflow-hidden">
                <img src="static/images/{nota['imagen']}" class="max-h-full max-w-full object-contain" alt="{nota['titulo']}">
            </div>
            <div class="p-4">
                <span class="text-purple-400 text-[10px] font-black uppercase tracking-widest">{nota['seccion']}</span>
                <h3 class="text-white font-bold text-lg mt-1 leading-tight line-clamp-2">{nota['titulo']}</h3>
                <p class="text-slate-400 text-xs mt-2 line-clamp-2">{nota['resumen']}</p>
                <a href="{nota['url']}" class="inline-block mt-4 text-purple-400 text-xs font-black uppercase hover:underline">Leer más →</a>
            </div>
        </div>
        """

    with open("template_portada.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(plantilla.replace("{{TARJETAS}}", html_tarjetas))
    print("🏠 Portadas actualizadas.")


if __name__ == "__main__":
    carpetas_web = ["codigorojo", "tijuana", "rosarito", "tecate", "empleos"]
    if len(sys.argv) > 1:
        generar_nota(sys.argv[1])
    else:
        for c in carpetas_web:
            ruta_c = os.path.join("content", c)
            if os.path.exists(ruta_c):
                for f in os.listdir(ruta_c):
                    if f.endswith(".md"):
                        generar_nota(os.path.join(ruta_c, f))
        generar_portadas(carpetas_web)
