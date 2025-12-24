<?php
// Forzar que el sistema reconozca acentos y ñ
header('Content-Type: text/html; charset=utf-8');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $titulo = htmlspecialchars($_POST['titulo'], ENT_QUOTES, 'UTF-8');
    $contenido = htmlspecialchars($_POST['contenido'], ENT_QUOTES, 'UTF-8');
    $seccion = $_POST['seccion'];
    $multimedia = $_POST['multimedia'];
    $redireccion = $_POST['redireccion'];
    $fecha = date("d/m/Y");

    // Detectar si es YouTube o Imagen
    if (strlen($multimedia) == 11) {
        $media_html = '<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;"><iframe src="https://www.youtube.com/embed/'.$multimedia.'" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" allowfullscreen></iframe></div>';
    } else {
        $media_html = '<img src="'.$multimedia.'" style="width:100%; display:block;">';
    }

    // Estructura de la tarjeta para tu columna única
    $nueva_nota = '
    <div class="card">
        ' . $media_html . '
        <div class="card-body">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span class="tag">' . strtoupper($seccion) . '</span>
                <span style="color:#888; font-size:12px;">' . $fecha . '</span>
            </div>
            <h2>' . $titulo . '</h2>
            <p>' . nl2br($contenido) . '</p>
            <div class="share-bar">
                <a href="' . $redireccion . '" style="color:#ffcc00; text-decoration:none; font-weight:bold;">LEER NOTA COMPLETA EN EL SITIO →</a>
                <a href="#top" style="color:#888; text-decoration:none; font-size:12px;">↑ SUBIR</a>
            </div>
        </div>
    </div>' . "\n";

    // Guardar la nota
    // Para que aparezca en el index.html, lo ideal es guardarlo en un archivo de datos o usar un marcador
    file_put_contents("../notas_recientes.html", $nueva_nota, FILE_APPEND);

    echo "<body style='background:#121212; color:white; font-family:sans-serif; text-align:center; padding:50px;'>";
    echo "<h1>🚀 ¡Nota publicada con éxito!</h1>";
    echo "<p>Se ha enviado a la sección: " . $seccion . "</p>";
    echo "<br><a href='index.php' style='color:#ffcc00; text-decoration:none; border:1px solid #ffcc00; padding:10px 20px; border-radius:5px;'>Volver al Panel</a>";
    echo "</body>";
}
?>
