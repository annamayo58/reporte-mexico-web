<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Multimedia - Reporte México</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.js"></script>
    <style>
        body { background: #121212; color: white; padding: 20px; }
        .panel-box { background: #1e1e1e; padding: 30px; border-radius: 15px; border: 1px solid #333; max-width: 800px; margin: auto; }
        label { color: #ffcc00; margin-top: 15px; display: block; }
        .form-control { background: #2a2a2a !important; color: white !important; border: 1px solid #444 !important; }
    </style>
</head>
<body>
<div class="panel-box">
    <h2 style="text-align:center;">🚀 POSTEAR NOTICIA MULTIMEDIA</h2>
    <form action="guardar_nota.php" method="POST">
        <div class="row">
            <div class="col-md-6">
                <label>📍 Sección:</label>
                <select name="seccion" class="form-control">
                    <option value="estados">Estados</option>
                    <option value="bienestar">Bienestar</option>
                    <option value="internacional">Internacional</option>
                    <option value="cultura">Cultura</option>
                    <option value="espectaculos">Espectáculos</option>
                </select>
            </div>
            <div class="col-md-6">
                <label>📅 Fecha:</label>
                <input type="text" name="fecha" class="form-control" value="<?php echo date('d/m/Y'); ?>" readonly>
            </div>
        </div>

        <label>📰 Título:</label>
        <input type="text" name="titulo" class="form-control" placeholder="Título del boletín..." required>

        <label>✍️ Contenido Enriquecido:</label>
        <textarea id="summernote" name="contenido"></textarea>

        <div class="row">
            <div class="col-md-6">
                <label>🖼️ URL Imagen (Opcional):</label>
                <input type="text" name="url_imagen" class="form-control" placeholder="https://link-de-la-foto.jpg">
            </div>
            <div class="col-md-6">
                <label>📺 ID YouTube (Opcional):</label>
                <input type="text" name="id_youtube" class="form-control" placeholder="Ej: dQw4w9WgXcQ">
            </div>
        </div>

        <label>🔗 Enlace de Redirección (Donde se leerá la nota completa):</label>
        <input type="text" name="redireccion" class="form-control" placeholder="https://sitio-destino.com/nota-completa" required>

        <button type="submit" class="btn btn-success btn-block" style="margin-top:20px; padding:15px; font-weight:bold;">✅ PUBLICAR EN LA RED</button>
    </form>
</div>
<script>
    $(document).ready(function() {
        $('#summernote').summernote({ height: 200, placeholder: 'Escribe aquí tu noticia...' });
    });
</script>
</body>
</html>
