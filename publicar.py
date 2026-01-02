def generar_nota(archivo_md):
    with open(archivo_md, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Extraemos metadatos de las primeras 4 líneas
    titulo = lineas[0].strip().replace('# ', '')
    imagen = lineas[1].strip()
    descripcion = lineas[2].strip()
    seccion = lineas[3].strip().lower() # Nueva línea para la sección
    cuerpo_md = "".join(lineas[4:])

    # Diccionario de colores para la barra de navegación
    colores_nav = {
        "codigo-rojo": "bg-red-900",     # Rojo oscuro
        "desaparecidos": "bg-slate-800", # Gris oscuro
        "tijuana": "bg-blue-900",        # Azul oscuro
        "default": "bg-slate-900"        # Color base
    }
    
    color_final = colores_nav.get(seccion, colores_nav["default"])
    contenido_html = markdown.markdown(cuerpo_md)

    with open('template.html', 'r', encoding='utf-8') as f:
        plantilla = f.read()

    # Realizamos los reemplazos en la plantilla
    final = plantilla.replace('{{CONTENIDO}}', contenido_html)
    final = final.replace('{{TITULO}}', titulo)
    final = final.replace('{{IMAGEN}}', imagen)
    final = final.replace('{{DESCRIPCION}}', descripcion)
    final = final.replace('{{NAV_COLOR}}', color_final) # ¡Aquí se activa el color!
    final = final.replace('{{ARCHIVO}}', archivo_md.replace('.md', ''))

    nombre_salida = archivo_md.replace('.md', '.html')
    with open(nombre_salida, 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"✅ Nota generada con éxito: {nombre_salida}")