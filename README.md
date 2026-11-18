# Verificación de la entrevista de Ángel Gaitán a Santiago Abascal

Web: **https://voodatari.github.io/verificacion-abascal/**

Ángel Gaitán entrevistó a Santiago Abascal (Vox), candidato a las elecciones generales del 29 de noviembre de 2026, con
preguntas recogidas entre sus trabajadores y seguidores
([vídeo en YouTube](https://www.youtube.com/watch?v=ghXykOJnWcI), 14 de noviembre de 2026, 1 h 4 min). Este repositorio
contiene la transcripción, las afirmaciones comprobables que hace el invitado, el veredicto de cada una con su explicación y
sus fuentes, y el código que genera la web.

Todo está aquí para que cualquiera pueda revisarlo, discutirlo y corregirlo.

> **Web no oficial.** No la han encargado ni respaldan Ángel Gaitán, su canal ni Vox. Es una verificación asistida por IA,
> sin revisión de un equipo de periodistas: «falso» significa que los datos contradicen lo dicho, no que haya intención de
> mentir. Los criterios y los límites están en [METODO.md](METODO.md).

## Resultado

24 afirmaciones comprobadas: 9 engañosas, 7 casi ciertas, 3 verdaderas, 5 no verificables y ninguna falsa. El detalle de cada
una (cita literal, minuto exacto del vídeo, explicación y fuentes) está en la web y en `entrevistas/abascal/resultados/`.

## De dónde sale el código

El generador de la web, la API abierta, el método y el diseño son del proyecto
[verificacion-podcast](https://github.com/PabloPC05/verificacion-podcast) de **Pablo Pardo Cotos** y **Diego Cristóbal
Andaluz** (web: https://verificacion-podcast.vercel.app), que verifica las entrevistas de The Wild Project a Pedro Sánchez,
Alberto Núñez Feijóo y Ada Colau. Esta es una adaptación a otra entrevista: se han quitado sus entrevistas, su marca y su
alojamiento en Vercel, y se ha cambiado lo que hacía falta para publicar en GitHub Pages y transcribir en Windows. Ellos no
han participado ni han revisado esta adaptación.

El repositorio original no declara ninguna licencia. Si eres autor del proyecto original y prefieres que esto se retire o se
cambie, abre una incidencia.

## Qué hay

| Carpeta | Contenido |
|---|---|
| `entrevistas/abascal/transcripcion.txt` | Transcripción automática completa, con marcas de tiempo. |
| `entrevistas/abascal/segmentos.json` | La misma transcripción por segmentos, con el segundo de inicio y fin. |
| `entrevistas/abascal/capitulos.json` | Capítulos del vídeo en YouTube. |
| `entrevistas/abascal/hablantes.json`, `transcripcion-hablantes.txt` | La voz de cada segmento (Ángel Gaitán, Santiago Abascal) y la transcripción por intervenciones. |
| `entrevistas/abascal/resultados/*.json` | Las afirmaciones verificadas, un fichero por bloque temático: cita literal, veredicto, explicación, confianza y fuentes. |
| `entrevistas/abascal/resumenes/*.json` | Resumen de una frase de cada explicación (el texto corto que muestra la web). |
| `entrevistas/abascal/esencial.json` | «Lo esencial»: las 5 afirmaciones clave y por qué. |
| `entrevistas/abascal/otros_verificadores.json` | Lo que otro verificador publicó sobre el mismo dato. |
| `entrevistas/temas.json`, `archivo.json`, `glosario.json` | Temas comunes entre entrevistas (vacío con una sola), copias archivadas de las fuentes y correcciones de nombres. |
| `herramientas/transcribir.py` | Descarga el audio y lo transcribe en local con Whisper (faster-whisper). |
| `herramientas/hablantes.py` | Reconoce quién habla en cada segmento, en local. |
| `herramientas/comprobar_datos.py` | Valida los JSON. |
| `herramientas/imagenes_compartir.py` | Genera las imágenes de vista previa para redes. |
| `web-src/build.py` | Genera la web estática (`web/`) a partir de los datos. Sin dependencias. |
| `METODO.md` | El procedimiento, los criterios de cada veredicto y los límites. La web lo publica en `/metodologia`. |

## API abierta

Los datos se publican también como JSON estático, sin clave y con CORS abierto. Documentación:
https://voodatari.github.io/verificacion-abascal/api

| Qué | Dirección |
|---|---|
| Entrevistas, recuentos y temas | `/api/v1/entrevistas.json` |
| Todas las afirmaciones | `/api/v1/afirmaciones.json` (y `.csv`) |
| Afirmaciones de la entrevista | `/api/v1/abascal.json` |
| Transcripción con tiempos | `/api/v1/abascal/transcripcion.json` y `.txt` |
| OpenAPI 3.1 | `/api/v1/openapi.json` |
| Guía para modelos de lenguaje | `/llms.txt` |

## Generar la web en local

```sh
python herramientas/comprobar_datos.py          # valida los JSON
python web-src/build.py                         # regenera web/ a partir de los datos
```

La web se genera con las rutas de GitHub Pages (`/verificacion-abascal/…`). Para verla en local con esas rutas, copia `web/`
a una carpeta que se llame `verificacion-abascal` y sirve la que la contiene:

```sh
mkdir -p /tmp/sitio && cp -r web /tmp/sitio/verificacion-abascal
python -m http.server -d /tmp/sitio 8000        # y abre http://localhost:8000/verificacion-abascal/
```

Para repetir la transcripción y el reconocimiento de voces hace falta un entorno con `yt-dlp`, `faster-whisper`,
`sherpa-onnx`, `ffmpeg` y Node.js; los pasos están en [METODO.md](METODO.md).

## Corregir un error o contribuir

- **Avisar de un error:** en la página de cada afirmación, el botón «Avisar de un error» abre una incidencia de GitHub con la
  afirmación ya rellenada; solo pide una fuente.
- **Pull request:** los pasos y qué ficheros tocar están en [CONTRIBUTING.md](CONTRIBUTING.md).
