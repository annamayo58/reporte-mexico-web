import markdown
import os
from datetime import datetime


# 1. Función para extraer datos de los archivos .md para la portada
def obtener_datos_notas(carpetas):
    notas = []
    for carpeta in carpetas:
        ruta_carpeta = os.path.join("content", carpeta)
        if not os.path.exists(ruta_carpeta):
            continue
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(".md"):
                ruta_completa = os.path.join(ruta_carpeta, archivo)
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    lineas = [l.strip() for l in f.readlines() if l.strip()]
                if len(lineas) >= 4:
                    notas.append(
                        {
                            "titulo": lineas[0],
                            "imagen": lineas[1],
                            "resumen": lineas[2],
                            "seccion": lineas[3],
                            "url": archivo.replace(".md", ".html"),
                            "fecha": os.path.getmtime(ruta_completa),
                        }
                    )
    # Ordenar por fecha (la más reciente primero)
    return sorted(notas, key=lambda x: x["fecha"], reverse=True)


# 2. Función para generar la nota individual (Título centrado arriba)
def generar_nota(ruta_md, nombre_salida):
    with open(ruta_md, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    titulo, imagen, descripcion = lineas[0], lineas[1], lineas[2]
    cuerpo_md = "\n\n".join(lineas[4:])
    contenido_html = markdown.markdown(cuerpo_md)

    with open("template.html", "r", encoding="utf-8") as f:
        plantilla = f.read()

    # Reemplazo de etiquetas en la plantilla de la nota
    final = (
        plantilla.replace("{{TITULO}}", titulo)
        .replace("{{IMAGEN}}", imagen)
        .replace("{{DESCRIPCION}}", descripcion)
        .replace("{{CONTENIDO}}", contenido_html)
    )

    with open(nombre_salida, "w", encoding="utf-8") as f:
        f.write(final)


# 3. Bloque Principal: Publicación de una nota y actualización de portada
if __name__ == "__main__":
    print("\n--- GENERADOR QUIRÚRGICO DE NOTICIAS ---")
    archivo_objetivo = input("Nombre del archivo .md (ej: nota2.md): ")
    ruta_target = os.path.join("content", "codigorojo", archivo_objetivo)

    if os.path.exists(ruta_target):
        # A. Generar la Nota Individual
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_html = f"{fecha_hoy}-01.html"
        # Evitar sobrescribir si publicas varias el mismo día
        contador = 1
        while os.path.exists(nombre_html):
            contador += 1
            nombre_html = f"{fecha_hoy}-{contador:02d}.html"

        generar_nota(ruta_target, nombre_html)
        print(f"✅ Nota creada: {nombre_html}")

        # B. Actualizar Portada Automáticamente (Tarjetas Clicables)
        carpetas_web = [
            "codigorojo",
            "tijuana",
            "rosarito",
            "tecate",
            "desaparecidos",
            "empleos",
        ]
        notas_lista = obtener_datos_notas(carpetas_web)

        html_tarjetas = ""
        for n in notas_lista[:12]:
            # Diseño de Tarjeta: TODO el bloque <a> es clicable
            html_tarjetas += f"""
            <a href="{n['url']}" class="group block bg-slate-800 rounded-xl overflow-hidden shadow-lg hover:scale-[1.02] transition-all duration-300 border border-slate-700">
                <div class="w-full h-48 bg-[#111827] overflow-hidden">
                    <img src="static/images/{n['imagen']}" 
                         class="w-full h-full object-cover group-hover:opacity-80 transition-opacity" 
                         alt="{n['titulo']}">
                </div>
                <div class="p-5">
                    <span class="text-purple-400 text-[10px] font-black uppercase tracking-widest">{n['seccion']}</span>
                    <h3 class="text-white font-bold text-xl mt-2 leading-tight group-hover:text-purple-400 transition-colors">
                        {n['titulo']}
                    </h3>
                    <p class="text-slate-400 text-sm mt-3 line-clamp-2 leading-relaxed">
                        {n['resumen']}
                    </p>
                    <div class="mt-4 text-purple-400 text-lg font-black uppercase tracking-wider flex items-center group-hover:translate-x-2 transition-transform">
                        LEER MÁS <span class="ml-2">→</span>
                    </div>
                </div>
            </a>
            """

        # C. Escribir el index.html final
        with open("template_portada.html", "r", encoding="utf-8") as f:
            plantilla_p = f.read()

        index_final = plantilla_p.replace("{{TARJETAS}}", html_tarjetas)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(index_final)

        print(f"✅ Portada 'index.html' actualizada con tarjetas clicables.")
    else:
        print(f"❌ Error: El archivo '{ruta_target}' no existe.")
