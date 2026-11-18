# Método de verificación

Este es el procedimiento con el que se ha verificado la entrevista de Ángel Gaitán a Santiago Abascal. Está escrito
para que cualquiera (una persona o una sesión de Claude Code) lo repita con otra entrevista y obtenga un resultado
comparable. Parte del método del proyecto original, [Verificación de las entrevistas electorales de The Wild Project](https://github.com/PabloPC05/verificacion-podcast),
de Pablo Pardo Cotos y Diego Cristóbal Andaluz; las diferencias están marcadas en cada paso. La regla principal:
**la misma vara de medir para todos los invitados, sea cual sea su partido.**

## 1. Descargar y transcribir

```sh
python -m venv .venv
.venv/Scripts/pip install yt-dlp faster-whisper pillow sherpa-onnx "av==15.1.0" nvidia-cublas-cu12 nvidia-cudnn-cu12
.venv/Scripts/python herramientas/transcribir.py <slug> <url-de-youtube> "<Nombre del invitado>" "<glosario opcional>"
```

Descarga el audio y lo transcribe en local con Whisper (`large-v3-turbo`, con `faster-whisper`; usa la GPU NVIDIA si hay
y, si no, la CPU). Crea `entrevistas/<slug>/` con la transcripción (`transcripcion.txt`, párrafos de ~1 minuto con marca
`[h:mm:ss]`), los segmentos con tiempos (`segmentos.json`), los capítulos del vídeo (`capitulos.json`), `info.txt` y
`meta.json`. Revisa `meta.json` (nombre del invitado, entrevistador, programa, fecha, duración). El audio
(`entrevista.m4a`) se queda en esa carpeta, pero no se sube al repo. `yt-dlp` necesita Node.js para extraer de YouTube.

*Diferencia con el original:* el proyecto original transcribe con `mlx-whisper`, que solo funciona en Mac con Apple Silicon.
Aquí se usa `faster-whisper`, con el mismo modelo y el mismo formato de salida.

## 1 bis. Reconocer quién habla

```sh
.venv/Scripts/python herramientas/hablantes.py <slug> [umbral]
```

Whisper transcribe pero no dice quién habla, así que este paso atribuye cada segmento de la transcripción a una voz, en
local. Parte del audio y de `segmentos.json` y necesita `ffmpeg`, `sherpa-onnx` y el modelo de huella de voz TitaNet-large
en `.modelos/` (el enlace de descarga está en la cabecera del script).

Antes hay que añadir en `MUESTRAS`, para la entrevista nueva, fragmentos escuchados a mano en los que hable una sola
persona: el entrevistador (`J`) y una respuesta larga del invitado (`G`).

1. Se calcula la huella de voz de cada segmento; los de menos de 1,2 s se amplían por los dos lados hasta 1,2 s.
2. Cada huella se compara con las muestras del entrevistador y del invitado, que se recalibran dos veces con los
   segmentos largos y claros.
3. Si el segmento no se parece lo bastante a ninguna queda como «Voz sin identificar» (cortes, público). El umbral es
   0,25 y se puede cambiar con el segundo argumento.
4. Un segmento de menos de 1,5 s y dudoso, entre dos del mismo hablante, toma la etiqueta de esos dos.

Escribe `hablantes.json` (la voz de cada segmento con sus puntuaciones, el tiempo total de cada voz y un campo `metodo`)
y `transcripcion-hablantes.txt` (la transcripción por intervenciones). La web los usa para mostrar la transcripción por
voces, y la API publica el hablante de cada segmento. **El acierto no se ha medido en esta entrevista**: en la del
proyecto original, con el mismo método, fue del 96,8 % en 125 segmentos etiquetados a mano. Los fallos esperables son
frases de menos de 1,5 segundos y segmentos en los que Whisper juntó a los dos hablantes.

## 2. Repartir por temas

Lee la transcripción entera y `capitulos.json`. Agrupa los capítulos en bloques temáticos (en esta entrevista, 23
capítulos del vídeo en 7 bloques: los capítulos sin datos comprobables se juntan). Para cada bloque anota el tramo de
tiempo y la lista de afirmaciones comprobables que haces a primera lectura.

## 3. Verificar

Se comprueba con búsqueda web cada afirmación FACTUAL COMPROBABLE que haga el invitado (no las del entrevistador, ni las
opiniones, valoraciones, promesas o anécdotas privadas imposibles de comprobar). El criterio es el del encargo original,
que sigue siendo la referencia si alguien repite el paso con subagentes:

> Eres verificador de datos (fact-checker) riguroso e imparcial. Hoy es `<fecha>`. `<Contexto: programa, invitado, fecha de
> publicación, elecciones>`. Tengo la transcripción automática (Whisper) en `<ruta>/transcripcion-hablantes.txt`, con marcas
> [h:mm:ss] al inicio de cada intervención y el nombre de quien habla.
>
> TAREA: comprueba con búsqueda web cada afirmación FACTUAL COMPROBABLE que haga `<INVITADO>` (no las del
> entrevistador). No evalúes opiniones, valoraciones, promesas ni anécdotas privadas imposibles de comprobar.
>
> MÉTODO: usa WebSearch y WebFetch. Muchos hechos son recientes: NO te fíes de tu memoria, búscalo. Prioriza fuentes
> primarias y oficiales (INE, Eurostat, BOE, Banco de España, Congreso, ministerios, resoluciones judiciales) y prensa de
> distintas líneas editoriales; verificadores (Newtral, Maldita, EFE Verifica) como apoyo. Aplica la misma vara de medir
> que a cualquier político de cualquier partido. Admite el redondeo razonable del lenguaje oral. Respeta la presunción de
> inocencia de los no condenados. Cita solo URLs que hayas visto de verdad; nunca inventes una URL ni un dato. Si no
> encuentras prueba suficiente, el veredicto es «no_verificable»: no fuerces ni «falso» ni «verdadero».
>
> VEREDICTOS: verdadero | mayormente_verdadero | enganoso (dato real pero sin contexto, mezcla de periodos o conclusión que
> no se sigue) | falso | no_verificable.
>
> ENTREGA: un array JSON de objetos `{"minuto": "h:mm:ss", "cita": "literal de la transcripción", "afirmacion":
> "reformulada y autocontenida", "veredicto": "...", "explicacion": "2-4 frases con el dato real, su fecha y de dónde
> sale", "confianza": "alta|media|baja", "fuentes": [{"titulo": "...", "url": "https://..."}]}`. Todo en español.

La `cita` debe ser literal: la web la usa para encontrar el segundo exacto del vídeo.

*Diferencia con el original:* el proyecto original lanzó un subagente por bloque temático. En esta entrevista no se lanzó
ninguno: una sola sesión de Claude Code (Sonnet) leyó la transcripción entera y comprobó cada afirmación con búsquedas web,
y después se escribieron los ficheros de `resultados/` con un script. Cuando un hecho dependía de una cifra que ninguna
fuente confirmaba, el veredicto es «no verificable» y la explicación dice qué se buscó. Las URL de las fuentes son las que
devolvió la búsqueda o que se abrieron; no todas se leyeron enteras, y la confianza de cada afirmación lo refleja.

Una afirmación solo se evalúa si la dice el invitado. Si una frase falsa o dudosa la dice el entrevistador y el invitado
solo contesta (por ejemplo, la pregunta sobre la UME en la DANA), no entra, aunque el invitado la acepte.

## 4. Resumir las justificaciones

Para cada afirmación, en el mismo orden, un resumen de la explicación: una frase (dos como mucho), máximo 30 palabras,
que empiece por el dato real y no añada nada que no esté en la explicación. Se guarda como array de cadenas en
`entrevistas/<slug>/resumenes/<NN-tema>.json` (misma longitud y orden que el fichero de resultados).

## 4 bis. Excluir lo que no aporta al debate público

Algunas afirmaciones se pueden comprobar pero no tienen interés público. Se quitan de la web y de los recuentos, y se
listan en `entrevistas/<slug>/excluidas.json` con su veredicto original y el motivo. La API las publica aparte, en el
campo `excluidas`. Solo hay seis motivos posibles:

| Motivo | Ejemplos |
|---|---|
| Dato biográfico o familiar del invitado | Edad, edad de los padres, hijos, estudios, idiomas, a quién votó en su juventud |
| Anécdota personal o privada | Qué coche usaba, qué redes sociales usa, ofertas de cargos que rechazó |
| Duración de un cargo o de una trayectoria | «Lleva ocho años en el Gobierno», «llevo 30 años en política» |
| Detalle logístico de la campaña o de la entrevista | Cuándo empieza la campaña, a qué medios ha ido, cuánto duró otra entrevista |
| Curiosidad sin relación con el debate público | Que el Papa votó, en qué año se construyó un edificio |
| Estimación dicha de pasada al hablar, con el dato de fondo verificado aparte | «19 semanas, que son 100 días», cuando el permiso de 19 semanas ya está verificado en otra afirmación |

El criterio se aplica igual a todos los invitados y **sin mirar el veredicto**. Nunca se excluye una afirmación sobre
políticas, cifras públicas, instituciones, leyes o la actuación de un cargo o de un partido, aunque parezca menor. En la
entrevista de Abascal no se llegó a verificar su relato biográfico (ETA, protección policial, licencia de armas) ni lo que
cuenta de la entrevista de La Revuelta: son hechos personales o logísticos, y por eso `excluidas.json` está vacío. Los
identificadores (`m<segundo>`) se asignan antes de excluir, así que no cambian.

## 5. Generar la web y publicar

Cuando todos los bloques y resúmenes estén completos y `python3 herramientas/comprobar_datos.py` no dé errores (valida los
JSON, los veredictos y que cada resumen case con su afirmación), añade `"publicar": true` a `entrevistas/<slug>/meta.json`
(el generador ignora las entrevistas que no lo tienen, para no publicar verificaciones a medias).

Antes de generar la web, crea las imágenes que se ven al compartir los enlaces (vista previa en WhatsApp, X, Telegram,
LinkedIn, Bluesky): una por entrevista y una por afirmación. Necesita Pillow y escribe en `web-src/compartir/`; hay que
subir esos ficheros al repositorio. Si falta la imagen de una entrevista, `build.py` avisa y usa la general.

```sh
.venv/Scripts/python herramientas/imagenes_compartir.py   # web-src/compartir/<slug>.png, 1200×630
python web-src/build.py                                   # genera toda la web en web/ (páginas, API y sitemap)
git add -A && git commit -m "Verificación de la entrevista a <invitado>" && git push
```

La web se publica en **GitHub Pages**: el flujo `.github/workflows/publicar.yml` ejecuta `build.py` en cada `push` a `main`
y despliega la carpeta `web/`. En el repositorio, en Settings → Pages, el origen tiene que ser «GitHub Actions».

*Diferencia con el original:* el proyecto original se publica en Vercel, desde la carpeta `web/` ya generada y con una
función para los formularios. Aquí la web vive en una subcarpeta (`/verificacion-abascal/`), así que `build.py` escribe las
rutas como si fuera un dominio propio y, al terminar, antepone el prefijo a todas (`prefijar_rutas()`, `RUTA_BASE`). Los
avisos de error y las propuestas son incidencias de GitHub (plantillas en `.github/ISSUE_TEMPLATE`), no formularios propios,
y no hay estadísticas de visitas. La API está en `web/api/` (la documentación en `/api` y los datos en `/api/v1/…`).

### Después de publicar

Estos pasos añaden contexto sin tocar los veredictos:

- **Copias archivadas de las fuentes.** `python3 herramientas/archivar_fuentes.py` guarda cada fuente en la Wayback Machine
  y lo apunta en `entrevistas/archivo.json`. La web pone «copia archivada» al lado de cada fuente. Todavía no se ha ejecutado
  con esta entrevista.
- **Lo esencial.** `entrevistas/<slug>/esencial.json` elige de 3 a 5 afirmaciones por candidato: las que llevan un dato
  concreto sobre los temas centrales de la campaña, salgan bien o mal. El criterio es el mismo para todos.
- **Otros verificadores.** `entrevistas/<slug>/otros_verificadores.json` enlaza lo que Newtral, Maldita.es, EFE Verifica u
  otros verificadores profesionales publicaron sobre la misma frase (`misma_frase`) o sobre el mismo dato dicho por el
  candidato en otro momento (`mismo_dato`). Un artículo general sobre el tema no cuenta, y su veredicto se copia tal cual,
  aunque no coincida con el nuestro. En esta entrevista solo hay piezas de elDiario.es, que comprobó lo que Abascal dijo en
  La Revuelta; no se ha encontrado ninguna de Newtral ni de Maldita.es sobre esta entrevista.
- **Temas comunes.** `entrevistas/temas.json` agrupa capítulos de las distintas entrevistas en temas compartidos para la
  comparativa de `/temas`. Un tema solo sale si lo tratan dos candidatos o más; con una sola entrevista no hay ninguno.

### Correcciones

Cuando una corrección cambia un veredicto, la explicación o una fuente, se edita la afirmación y se le añade
`correcciones: [{fecha, antes, motivo}]`. La web la marca como «Corregido» y enseña el historial en su página, con el
veredicto anterior a la vista, y la API lo publica en el mismo campo. Cada afirmación muestra además la fecha en que se
verificó (`verificado` en `meta.json`, o en la propia afirmación si se volvió a verificar entera).

Esta página (`/metodologia`) sale de este mismo fichero, `METODO.md`: para cambiar el método, se edita aquí y se vuelve a
ejecutar `build.py`.

## Qué significa cada veredicto

| Veredicto | Criterio |
|---|---|
| Verdadero | Los datos lo confirman. |
| Casi cierto | Cierto en lo esencial, con una imprecisión menor. |
| Engañoso | Se apoya en algo real pero omite contexto, mezcla periodos o lleva a una conclusión que no se sigue. |
| Falso | Los datos lo contradicen. No implica intención de mentir: incluye errores y lapsus. Las estimaciones dichas de pasada cuyo dato de fondo ya se verifica aparte se excluyen (apartado 4 bis). |
| No verificable | No hay prueba pública suficiente, o la búsqueda se quedó corta. |

## Límites conocidos

- La verificación la hace un modelo de IA y no la revisa un equipo de periodistas.
- Es una sola entrevista de una hora: 24 afirmaciones comprobadas no son todo lo que se dijo. Se eligieron las que tienen un
  dato público contrastable; el resto (opiniones, promesas, anécdotas) no se evalúa.
- La herramienta de búsqueda devuelve resúmenes y no siempre permite abrir la fuente primaria. Una parte de las
  afirmaciones queda como «no verificable» o con confianza baja por ese motivo, no porque sean falsas.
- La transcripción automática a veces confunde nombres y cifras (por ejemplo, «La Habana» donde por el contexto debería
  decir otra cosa). La atribución de cada frase a su hablante también es automática y no se ha medido en esta entrevista.
- Los veredictos dependen de la fecha: los datos de vivienda, empleo y encuestas cambian, y los que cita esta web son de
  noviembre de 2026.

Para proponer una corrección, mira [CONTRIBUTING.md](CONTRIBUTING.md).
