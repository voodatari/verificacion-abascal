"""Página /participa. Los avisos de error y las propuestas de hechos a verificar son incidencias de GitHub (plantillas en
.github/ISSUE_TEMPLATE). En las dos, el enlace a una fuente de contraste es obligatorio. La importa build.py.
"""

ESTILO = """:root { --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif; }
* { box-sizing:border-box; }
body { margin:0; background:var(--fondo); color:var(--tinta); font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
a { color:var(--tinta); text-underline-offset:3px; }
main.ancho { padding-bottom:72px; }
/* Página de lectura: una columna centrada, como el método o una afirmación */
.columna { max-width:780px; margin:0 auto; padding-top:clamp(28px,5vw,56px); }
h1 { font:700 clamp(30px,5.2vw,58px)/1.05 var(--serif); letter-spacing:-0.02em; margin:0 0 14px; text-wrap:balance; }
.entrada { font-size:17px; max-width:62ch; margin:0 0 28px; color:var(--suave); }
.caja { border:2px solid var(--tinta); border-radius:var(--r-caja); padding:clamp(16px,2.4vw,24px); margin:0 0 22px; }
.rot { margin:0 0 4px; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--gris); }
#sobre p:not(.rot) { margin:0 0 6px; font:700 20px/1.3 var(--serif); }
form { display:grid; gap:20px; }
.campo { display:grid; gap:6px; font-weight:700; }
.campo .ayuda { font-weight:400; font-size:14.5px; color:var(--suave); max-width:68ch; }
.oblig { font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.08em; color:var(--gris); margin-left:6px; }
input, textarea { font:inherit; font-weight:400; color:var(--tinta); background:var(--fondo); width:100%; min-height:46px;
  border:2px solid var(--tinta); border-radius:var(--r-boton); padding:10px 12px; }
textarea { resize:vertical; line-height:1.5; }
[aria-invalid=true] { border-color:var(--v-falso); }
.error { margin:-10px 0 0; color:var(--v-falso); font-weight:600; font-size:15px; }
.trampa { position:absolute; left:-9999px; width:1px; height:1px; overflow:hidden; }
.enviar { justify-self:start; min-height:46px; padding:0 22px; font:inherit; font-weight:700; cursor:pointer;
  background:var(--tinta); color:var(--fondo); border:2px solid var(--tinta); border-radius:var(--r-boton); }
.enviar:hover { background:var(--fondo); color:var(--tinta); }
.enviar:disabled { opacity:.6; cursor:progress; }
.privacidad { margin:0; font-size:14px; color:var(--suave); max-width:68ch; }
.hecho h2 { font:700 clamp(24px,2.4vw,28px)/1.2 var(--serif); margin:0 0 8px; }
.hecho p { margin:0 0 10px; max-width:68ch; }
@media (max-width:560px) { .enviar { justify-self:stretch; } }
.otro { margin:-12px 0 28px; font-size:15px; max-width:68ch; }
select { font:inherit; font-weight:400; color:var(--tinta); background:var(--fondo); width:100%; min-height:46px; border:2px solid var(--tinta); border-radius:var(--r-boton); padding:8px 12px; }
.dos { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr)); gap:20px; }
.dos > * { min-width:0; }
"""

PARTICIPA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
@@HEAD_MODO@@
@@CABECERA@@
<style>
@@ESTILO_FORM@@
.cabeza { padding:clamp(28px,5vw,56px) 0 clamp(24px,3vw,36px); }
.cabeza h1 { margin:0 0 14px; }
.cabeza .entrada { margin:0; }
@media (min-width:1000px) { .cabeza { display:grid; grid-template-columns:minmax(0,1.2fr) minmax(0,1fr); gap:0 clamp(32px,5vw,80px); align-items:end; }
  .cabeza h1 { margin:0; } }
.vias { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr)); gap:clamp(16px,2vw,24px); margin:0 0 clamp(36px,5vw,56px); }
.via { display:flex; flex-direction:column; gap:12px; min-width:0; margin:0; }
.via h2 { font:700 clamp(24px,2.4vw,28px)/1.2 var(--serif); margin:0; text-wrap:balance; }
.via p { margin:0; max-width:62ch; }
.via .atajo { font-size:14.5px; color:var(--suave); }
.via .boton { margin-top:auto; align-self:flex-start; display:inline-flex; align-items:center; min-height:46px; padding:0 22px; font-weight:700;
  text-decoration:none; background:var(--tinta); color:var(--fondo); border:2px solid var(--tinta); border-radius:var(--r-boton);
  transition:background-color .18s ease-out, color .18s ease-out; }
.via .boton:hover { background:var(--fondo); color:var(--tinta); }
@media (max-width:560px) { .via .boton { align-self:stretch; justify-content:center; } }
.despues { border-top:3px solid var(--tinta); padding-top:12px; }
.despues h2 { font:700 clamp(24px,2.4vw,28px)/1.2 var(--serif); margin:0 0 14px; }
.despues ul { margin:0 0 18px; padding-left:20px; max-width:68ch; }
.despues li { margin:0 0 8px; }
.despues .registro { margin:0; max-width:68ch; }
</style>
<style>@@CSS_MENU@@</style>
</head>
<body>
@@MENU@@
<main class="ancho">
<div class="cabeza">
<h1>Participa</h1>
<p class="entrada">Esta verificación la hace una IA y la mejoramos con lo que nos mandáis. Hay dos formas de ayudar y, en las dos, te pedimos un enlace a una fuente: así cualquiera puede comprobarlo. No hace falta cuenta.</p>
</div>

<div class="vias">
<section class="caja via" aria-labelledby="via-error">
<p class="rot">Corregir</p>
<h2 id="via-error">¿Hemos verificado algo mal?</h2>
<p>Si crees que un veredicto es incorrecto, mándanos el enlace a una web que muestre el dato correcto. Lo revisamos con el mismo criterio para todos los partidos.</p>
<p class="atajo">Atajo: en cada afirmación, el botón «Avisar de un error» abre la incidencia con ella ya puesta.</p>
<a class="boton" href="@@REPO@@/issues/new?template=correccion.yml" target="_blank" rel="noopener noreferrer">Avisar de un error</a>
</section>
<section class="caja via" aria-labelledby="via-propuesta">
<p class="rot">Añadir</p>
<h2 id="via-propuesta">¿Falta algo que se dijo?</h2>
<p>Si el entrevistado dijo algo comprobable que no está en la línea temporal, cuéntanos qué dijo y en qué minuto, con un enlace para contrastarlo.</p>
<p class="atajo">Escribe quién lo dijo, el minuto y el enlace a una fuente.</p>
<a class="boton" href="@@REPO@@/issues/new?template=propuesta.yml" target="_blank" rel="noopener noreferrer">Proponer un hecho para verificar</a>
</section>
</div>

<section class="despues" aria-labelledby="despues">
<h2 id="despues">Qué pasa después</h2>
<ul>
<li>Tu envío se publica tal cual en el registro público del proyecto, en GitHub, sin ningún dato tuyo. No pongas datos personales.</li>
<li>Lo revisamos con el <a href="/metodologia">mismo método</a> y la misma vara de medir para todos los partidos.</li>
<li>Si la fuente lo confirma, corregimos el veredicto o añadimos la afirmación, y el cambio queda registrado.</li>
</ul>
<p class="registro">Puedes seguir cómo se resuelve cada uno: <a href="@@REPO@@/issues?q=is%3Aissue+label%3Acorrecci%C3%B3n" target="_blank" rel="noopener noreferrer">avisos de error</a> y <a href="@@REPO@@/issues?q=is%3Aissue+label%3Apropuesta" target="_blank" rel="noopener noreferrer">propuestas</a>.</p>
</section>
</main>
<footer class="pie-solo"><div class="ancho">@@PIE@@</div></footer>
</body>
</html>
"""
