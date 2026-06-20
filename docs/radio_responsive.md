\# Radio Responsive — HB Jewelry



\## Objetivo

Módulo de difusión multicanal con adaptación automática

por dispositivo y plataforma de destino.



\## Canales activos

\- WhatsApp Business API

\- Instagram DM + Stories

\- Email campañas

\- SMS (pendiente activación Railway)



\## Lógica responsive por canal

Cada pieza de contenido se adapta automáticamente:



| Canal      | Formato      | Dimensión    | Duración |

|------------|--------------|--------------|----------|

| Instagram  | Reel/Story   | 9:16         | 8-30s    |

| WhatsApp   | Video/Imagen | 1:1 o 16:9   | <16MB    |

| Email      | Banner       | 600px ancho  | —        |

| SMS        | Texto        | <160 chars   | —        |



\## Arquitectura de nodos



\### Nodo 1 — Input

Acepta tres tipos de entrada:

\- Texto: prompt o descripción del producto

\- Imagen: foto del producto (jpg/png <5MB)

\- Video: clip base para reencuadrar



Endpoint:

POST /api/radio/input

{ tipo: "texto|imagen|video", contenido, producto\_id }



\### Nodo 2 — Procesador IA

Flujo según tipo de input:



texto  → Veo 3.1 genera clip 8s + audio

imagen → Veo 3.1 photo-to-video + Canva overlay

video  → reencuadre por canal + compresión



Reglas de procesamiento:

\- Siempre generar versión 9:16 (móvil primero)

\- Siempre generar versión 1:1 (WhatsApp/Feed)

\- Audio: mantener si existe, generar si no

\- Marca HB Jewelry: overlay automático Canva API



\### Nodo 3 — Scheduler

Conectado al calendario 30 días (Tarea A).

Cada entrada del calendario puede tener:

{ ..., video\_generado: true, clip\_url, estado: "pendiente|listo|publicado" }



Endpoint:

POST /api/radio/schedule

{ plantilla\_id, canal, fecha\_publicacion }



\### Nodo 4 — Output

Publica o encola según canal:



Instagram → Graph API (video + caption + hashtags)

WhatsApp  → Business API (media message)

Email     → adjunto o link embed

SMS       → link corto al clip



Endpoint:

POST /api/radio/publish

{ clip\_id, canales\[], inmediato: bool }



\## Variables de entorno requeridas

GOOGLE\_VIDS\_API\_KEY=

CANVA\_API\_KEY=

VEO\_MODEL=veo-3.1-fast

RADIO\_STORAGE=google\_drive

DRIVE\_FOLDER\_ID=



\## Próximos pasos

\- \[ ] Conectar Google Vids API

\- \[ ] Conectar Canva API overlay

\- \[ ] Integrar con módulo Marketing existente

\- \[ ] Container radio-worker en docker-compose

\- \[ ] Endpoint batch para generar 30 clips del calendario

