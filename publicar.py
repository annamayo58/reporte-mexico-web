import markdown
import sys
import os


def generar_nota(ruta_archivo_md, recientes_html, nombre_salida):
    if not os.path.exists(ruta_archivo_md):
        return

    with open(ruta_archivo_md, "r", encoding="utf-8") as f:
        # Leemos todas las líneas y eliminamos espacios en blanco accidentales
        todas_las_lineas = [l.strip() for l in f.readlines()]
        # Filtramos para quedarnos solo con las que tienen contenido real
        lineas = [l for l in todas_las_lineas if l]

    if len(lineas) < 4:
        return

    # Extraemos datos basándonos en tu nuevo formato de texto plano
    titulo = lineas[0]
    imagen = lineas[1]
    descripcion = lineas[2]
    seccion = lineas[3].lower()

    # El cuerpo es todo lo que sobra después de los datos básicos
    # Buscamos dónde empieza el cuerpo real en el archivo original
    indice_cuerpo = (
        todas_las_lineas.index(seccion) + 1 if seccion in todas_las_lineas else 4
    )
    cuerpo_md = "\n\n".join(todas_las_lineas[indice_cuerpo:])
    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazo de etiquetas
    final = (
        plantilla.replace("{{TITULO}}", titulo)
        .replace("{{IMAGEN}}", imagen)
        .replace("{{DESCRIPCION}}", descripcion)
        .replace("{{CONTENIDO}}", contenido_html)
        .replace("{{RECIENTES}}", recientes_html)
    )

    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)

    # AQUÍ USAMOS EL NOMBRE AUTOMÁTICO (2026-01-02-01.html)
    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)

    nombre_base = os.path.basename(ruta_archivo_md).replace(".md", "")
    with open(f"{nombre_base}.html", "w", encoding="utf-8") as f:
        f.write(final)


def obtener_datos_notas(carpetas):
    notas = []
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
                    img = lineas[1].strip()
                    notas.append(
                        {
                            "titulo": lineas[0].strip().replace("# ", ""),
                            "imagen": (
                                img
                                if img and img.lower() != "ninguna"
                                else "logo-social.webp"
                            ),
                            "resumen": lineas[2].strip(),
                            "url": archivo.replace(".md", ".html"),
                            "seccion": carpeta,
                            "ruta_origen": os.path.join(ruta, archivo),
                        }
                    )
    return notas


def generar_sitio():
    carpetas_web = ["codigorojo", "tijuana", "rosarito", "tecate", "empleos"]
    todas_las_notas = obtener_datos_notas(carpetas_web)

    # Ordenar por las más nuevas (si quieres) o simplemente tomar las últimas 5
    recientes_html = ""
    for n in todas_las_notas[:6]:  # Mostramos las últimas 6 en la barra lateral
        recientes_html += f"""
        <a href="{n['url']}" class="group block border-b border-slate-800 pb-4 last:border-0">
            <span class="text-purple-400 text-[10px] font-black uppercase tracking-tighter">{n['seccion']}</span>
            <h4 class="text-white text-sm font-bold group-hover:text-purple-400 transition-colors leading-tight mt-1">
                {n['titulo']}
            </h4>
        </a>
        """

    # 1. Generar Notas Individuales
    for n in todas_las_notas:
        generar_nota(n["ruta_origen"], recientes_html)

    # 2. Generar Portada Principal (index.html)
    html_tarjetas += f"""
        <div class="bg-slate-800 rounded-lg overflow-hidden shadow-lg hover:scale-105 transition-transform border border-slate-700">
            <div class="w-full h-48 bg-[#111827] flex items-center justify-center overflow-hidden">
                <img src="static/images/{n['imagen']}" 
                     class="max-h-full max-w-full object-contain" 
                     alt="{n['titulo']}">
            </div>
            <div class="p-4">
                <span class="text-purple-400 text-[10px] font-black uppercase tracking-widest">{n['seccion']}</span>
                <h3 class="text-white font-bold text-lg mt-1 leading-tight line-clamp-2">{n['titulo']}</h3>
                <p class="text-slate-400 text-xs mt-2 line-clamp-2">{n['resumen']}</p>
                <a href="{n['url']}" class="inline-block mt-4 text-purple-400 text-xs font-black uppercase hover:underline">Leer más →</a>
            </div>
        </div>
        """

    with open("template_portada.html", "r", encoding="utf-8") as f:
        plantilla_p = f.read()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(plantilla_p.replace("{{TARJETAS}}", html_tarjetas))

    print("✅ Sitio completo actualizado con barra lateral.")


if __name__ == "__main__":
    from datetime import datetime

    # 1. Configuración de carpetas y recolección
    carpetas_web = [
        "codigorojo",
        "tijuana",
        "rosarito",
        "tecate",
        "desaparecidos",
        "empleos",
    ]
    notas_lista = obtener_datos_notas(carpetas_web)

    # 2. Generar Sidebar (Más Noticias)
    sidebar_html = ""
    for n in notas_lista[:6]:
        sidebar_html += f"""
        <a href="{n['url']}" class="group block border-b border-slate-800 pb-4 last:border-0">
            <span class="text-purple-400 text-[10px] font-black uppercase tracking-tighter">{n['seccion']}</span>
            <h4 class="text-white text-sm font-bold group-hover:text-purple-400 transition-colors mt-1">
                {n['titulo']}
            </h4>
        </a>
        """

    # 3. Generar Notas con Consecutivo (02012026_mx01.html)
    fecha_hoy = datetime.now().strftime("%d%m%Y")
    contador = 1

    for n in notas_lista:
        nuevo_nombre = f"{fecha_hoy}_mx{contador:02d}.html"
        generar_nota(n["ruta_origen"], sidebar_html, nuevo_nombre)
        n["url"] = nuevo_nombre  # Actualizamos para que la portada use el nuevo nombre
        contador += 1

    # 4. Generar la Portada (index.html)
    html_tarjetas = ""
    for n in notas_lista:
        html_tarjetas += f"""
        <div class="group bg-slate-800 rounded-lg overflow-hidden shadow-lg border border-slate-700">
            <div class="w-full h-48 bg-[#111827] flex items-center justify-center overflow-hidden">
                <img src="static/images/{n['imagen']}" 
                     class="max-h-full max-w-full object-contain transition-transform duration-500 group-hover:scale-110" 
                     alt="{n['titulo']}">
            </div>
            <div class="p-4">
                <span class="text-purple-400 text-[10px] font-black uppercase tracking-widest">{n['seccion']}</span>
                <h3 class="text-white font-bold text-lg mt-1 leading-tight line-clamp-2">{n['titulo']}</h3>
                <p class="text-slate-400 text-xs mt-2 line-clamp-2">{n['resumen']}</p>
                <a href="{n['url']}" class="inline-block mt-4 text-purple-400 text-xs font-black uppercase hover:underline">Leer más →</a>
            </div>
        </div>
        """

    with open("template_portada.html", "r", encoding="utf-8") as f:
        plantilla_p = f.read()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(plantilla_p.replace("{{TARJETAS}}", html_tarjetas))

    print(f"✅ ¡Éxito! Se generaron {len(notas_lista)} notas y la portada principal.")
if __name__ == "__main__":
    from datetime import datetime

    # 1. Configuración de carpetas y recolección
    carpetas_web = [
        "codigorojo",
        "tijuana",
        "rosarito",
        "tecate",
        "desaparecidos",
        "empleos",
    ]
    notas_lista = obtener_datos_notas(carpetas_web)

    # 2. Generar Sidebar (Más Noticias)
    sidebar_html = ""
    for n in notas_lista[:6]:
        sidebar_html += f"""
        <a href="{n['url']}" class="group block border-b border-slate-800 pb-4 last:border-0">
            <span class="text-purple-400 text-[10px] font-black uppercase tracking-tighter">{n['seccion']}</span>
            <h4 class="text-white text-sm font-bold group-hover:text-purple-400 transition-colors mt-1">
                {n['titulo']}
            </h4>
        </a>
        """

    # 3. Generar Notas con Formato YYYY-MM-DD-XX
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")  # Formato 2026-01-02
    contador = 1

    for n in notas_lista:
        # Generamos el nombre: 2026-01-02-01.html
        nuevo_nombre = f"{fecha_hoy}-{contador:02d}.html"
        generar_nota(n["ruta_origen"], sidebar_html, nuevo_nombre)

        n["url"] = nuevo_nombre  # El index usará este nuevo enlace
        contador += 1

    # 4. Generar la Portada (index.html) con el efecto Zoom
    html_tarjetas = ""
    for n in notas_lista:
        html_tarjetas += f"""
        <div class="group bg-slate-800 rounded-lg overflow-hidden shadow-lg border border-slate-700">
            <div class="w-full h-48 bg-[#111827] flex items-center justify-center overflow-hidden">
                <img src="static/images/{n['imagen']}" 
                     class="max-h-full max-w-full object-contain transition-transform duration-500 group-hover:scale-110" 
                     alt="{n['titulo']}">
            </div>
            <div class="p-4">
                <span class="text-purple-400 text-[10px] font-black uppercase tracking-widest">{n['seccion']}</span>
                <h3 class="text-white font-bold text-lg mt-1 leading-tight line-clamp-2">{n['titulo']}</h3>
                <p class="text-slate-400 text-xs mt-2 line-clamp-2">{n['resumen']}</p>
                <a href="{n['url']}" class="inline-block mt-4 text-purple-400 text-xs font-black uppercase hover:underline">Leer más →</a>
            </div>
        </div>
        """

    with open("template_portada.html", "r", encoding="utf-8") as f:
        plantilla_p = f.read()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(plantilla_p.replace("{{TARJETAS}}", html_tarjetas))

    print(
        f"✅ Éxito: Se generaron {len(notas_lista)} notas con formato {fecha_hoy}-XX.html"
    )
