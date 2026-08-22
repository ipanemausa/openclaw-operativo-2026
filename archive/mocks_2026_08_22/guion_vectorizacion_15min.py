#!/usr/bin/env python3
"""
====================================================================
 GUIÓN MAESTRO — VIDEO EDUCATIVO 15 MINUTOS
 "VECTORIZACIÓN: El Espacio Donde Vive el Significado"
 OpenClaw 2026.7.1 | Canal Educativo Guillermo
====================================================================
 Estructura: 5 bloques × 3 minutos
 Formato:    Teleprompter sync + B-Roll triggers + Edge-TTS 48kHz
====================================================================
"""

TITULO  = "Vectorización: El Espacio Donde Vive el Significado"
CANAL   = "OpenClaw Educativo"
VERSION = "2026.7.1"

# ─── 5 BLOQUES × 3 MINUTOS = 15 MINUTOS ─────────────────────────────────────

GUION = [

  # ══════════════════════════════════════════════════════════════════
  # BLOQUE 1 — EL PROBLEMA (0:00 – 3:00)
  # ══════════════════════════════════════════════════════════════════
  {
    "bloque": 1,
    "titulo": "El Problema — Las Máquinas No Leen",
    "duracion_min": 3,
    "broll_trigger": "coordenadas XYZ en pantalla",
    "texto": """
Hola, bienvenido. Soy Guillermo y hoy vamos a hablar de algo que parece
complicado pero en realidad es geometría que aprendiste en la escuela.

Antes de la inteligencia artificial, las computadoras eran muy literales.
Si buscabas la palabra "perro", no encontraba "can", ni "mascota", ni "labrador".
Buscaba exactamente esas cuatro letras: P-E-R-R-O.

El problema es que el lenguaje humano no funciona así.
Nosotros entendemos por contexto, por significado, no por caracteres exactos.

Entonces surgió la pregunta: ¿cómo le enseñamos a una máquina qué significa
una palabra? ¿Cómo le explicamos que "casa" y "hogar" son casi lo mismo,
pero "casa" y "automóvil" son muy diferentes?

La respuesta es tan elegante que cuando la entiendes no puedes dejar de pensar en ella.

La solución es convertir cada palabra, cada frase, cada documento
en una DIRECCIÓN en el espacio.

No en el espacio de 3 dimensiones que conocemos.
En un espacio de 768 dimensiones.

Y ahí está la magia.
""",
  },

  # ══════════════════════════════════════════════════════════════════
  # BLOQUE 2 — LAS DIMENSIONES (3:00 – 6:00)
  # ══════════════════════════════════════════════════════════════════
  {
    "bloque": 2,
    "titulo": "Las Dimensiones — De 3D a 768D",
    "duracion_min": 3,
    "broll_trigger": "diagrama 3D expandiéndose a 768D",
    "texto": """
Empecemos con lo que conoces.

El espacio físico tiene 3 dimensiones.
Tu silla en esta habitación tiene una posición exacta:
tres metros al frente, uno a la derecha, y a un metro del suelo.
Eso es X, Y, Z. Tres números. Una dirección única en el espacio.

Ahora imagina que en lugar de describir la posición física de un objeto,
describes el SIGNIFICADO de una palabra.

Para hacer eso, necesitas más dimensiones.
No 3. No 10. No 100. Necesitas 768.

¿Por qué 768? Porque el modelo de Google que usamos en nuestro sistema,
llamado text-embedding-004, fue entrenado con miles de millones de textos
y encontró que 768 coordenadas son suficientes para capturar
todos los matices del lenguaje humano.

Esto es lo que pasa cuando procesas la frase "automatización empresarial":

El modelo genera 768 números. Cada número representa una dimensión semántica.
Algunas dimensiones capturan si el concepto es técnico o emocional.
Otras si es positivo o negativo.
Otras si está relacionado con negocios, o tecnología, o arte.

El resultado es un punto único en ese espacio de 768 dimensiones.
Una dirección que ninguna otra frase en el idioma tiene exactamente igual.

Eso es un vector.
Eso es un embedding.
No es magia. Es geometría.
""",
  },

  # ══════════════════════════════════════════════════════════════════
  # BLOQUE 3 — LA DISTANCIA COSENO (6:00 – 9:00)
  # ══════════════════════════════════════════════════════════════════
  {
    "bloque": 3,
    "titulo": "La Distancia Coseno — Cómo Mide la IA el Significado",
    "duracion_min": 3,
    "broll_trigger": "dos vectores con ángulo entre ellos",
    "texto": """
Ahora que entiendes que cada frase es una dirección en el espacio,
la pregunta es: ¿cómo sabe la IA si dos frases son similares?

Con distancia. Igual que en geometría.

Pero no la distancia en línea recta que aprendiste de Pitágoras.
En vectores usamos la distancia coseno.

El coseno mide el ÁNGULO entre dos vectores.
Si dos flechas apuntan casi en la misma dirección, el ángulo es pequeño,
y el coseno es cercano a cero.
Si apuntan en direcciones opuestas, el ángulo es 180 grados,
y el coseno es cercano a 1.

Veamos en nuestro sistema real.

Tenemos tres frases vectorizadas en Firestore con 768 coordenadas cada una.

"Automatización de procesos con IA" — vector A.
"Agentes autónomos para empresas"   — vector B.
"Receta de pasta carbonara"         — vector C.

La distancia coseno entre A y B es 0.04.
Casi cero. Casi el mismo ángulo. Significado muy similar.

La distancia coseno entre A y C es 0.91.
Casi 1. Ángulo casi recto. Significados completamente diferentes.

Cuando tú le preguntas a nuestro sistema algo sobre automatización,
el sistema convierte tu pregunta a un vector,
calcula la distancia coseno con todos los documentos en Firestore,
y te devuelve los más cercanos.

No busca palabras. Busca vecinos en el espacio de 768 dimensiones.

Eso es lo que llamamos RAG: Retrieval Augmented Generation.
Recuperación aumentada por generación.
Tu pregunta en texto → vector → búsqueda geométrica → contexto relevante → respuesta.
""",
  },

  # ══════════════════════════════════════════════════════════════════
  # BLOQUE 4 — MÁS ALLÁ DEL TEXTO: VOZ, IMAGEN, VIDEO (9:00 – 12:00)
  # ══════════════════════════════════════════════════════════════════
  {
    "bloque": 4,
    "titulo": "Más Allá del Texto — Voz, Imagen y Video también son Vectores",
    "duracion_min": 3,
    "broll_trigger": "diagrama de modalidades: texto / voz / imagen / video",
    "texto": """
Aquí es donde se pone aún más interesante.

Los vectores no son solo para texto.

Tu VOZ es un vector.

Cuando grabas audio, tu computadora captura 48,000 muestras por segundo.
¿Por qué 48,000? Porque el oído humano percibe frecuencias hasta 20,000 hertz,
y el teorema de Nyquist dice que necesitas el doble de muestras
para reconstruir perfectamente cualquier sonido.
48 kilohertz. 48,000 coordenadas por segundo. Un vector de audio.

Cuando en nuestro sistema aplicamos EBU R128 a menos 14 LUFS,
estamos normalizando ese vector de audio a un volumen estándar internacional.
LUFS significa Loudness Units Full Scale.
Es la unidad de medida de intensidad percibida por el oído humano.
Menos 14 es el estándar de YouTube y Spotify.

Una IMAGEN es un vector.

Una imagen de 1920 por 1080 pixeles tiene 2,073,600 puntos.
Cada punto tiene tres valores: Rojo, Verde, Azul. RGB.
Eso es 6,220,800 números. Un vector de más de 6 millones de dimensiones.

Cuando aplicamos el filtro HSL 3D de fondo en nuestros videos,
estamos modificando los valores de Hue, Saturation y Lightness
en ese espacio de millones de dimensiones para crear el efecto visual.

La MEMORIA de la IA es un vector.

Los modelos de lenguaje como GPT o Gemini tienen lo que se llama contexto.
Ese contexto es una ventana de tokens, donde cada token es un fragmento de texto
convertido a vector. El límite de contexto es cuántos vectores caben en memoria
al mismo tiempo.

Cuando nuestro sistema RAG dice 97.66% de ahorro,
significa que comprimimos 474 kilobytes de documentos
a solo 11.5 kilobytes de vectores.
No perdemos información. La información está en la POSICIÓN.
En la dirección dentro del espacio semántico.
""",
  },

  # ══════════════════════════════════════════════════════════════════
  # BLOQUE 5 — APLICACIÓN PRÁCTICA Y CIERRE (12:00 – 15:00)
  # ══════════════════════════════════════════════════════════════════
  {
    "bloque": 5,
    "titulo": "La Aplicación Práctica — Por Qué Esto Cambia Tu Empresa",
    "duracion_min": 3,
    "broll_trigger": "diagrama del pipeline RAG completo OpenClaw",
    "texto": """
Muy bien. Ahora conectemos todo con tu empresa.

Si estás construyendo un sistema de IA, la pregunta no es
"¿uso IA sí o no?"

La pregunta es: ¿en qué espacio vectorial vive el conocimiento de mi empresa?

Tu catálogo de productos es un conjunto de vectores.
Las conversaciones con tus clientes son vectores.
Tus procesos operativos son vectores.
Los errores que ha tenido tu sistema son vectores.

Cuando tienes eso vectorizado en una base de datos como Firestore,
y conectas un modelo de lenguaje al frente,
el resultado es un sistema que puede responder preguntas sobre tu empresa
de la misma forma en que tú lo harías.

No porque memorizó el texto.
Sino porque navega geométricamente el espacio donde vive tu conocimiento.

En nuestro sistema OpenClaw:
El operador dice "AUDITA LA APP".
El sistema convierte esa frase a un vector de 768 dimensiones.
Busca los procesos más cercanos en el espacio semántico.
Ejecuta el script correspondiente.
Vectoriza el resultado en Firestore para memoria futura.

Automatización completa guiada por geometría.

Eso es lo que están haciendo las empresas más avanzadas del mundo hoy.
Y tú acabas de entender exactamente cómo funciona.

Hasta la próxima. Soy Guillermo.
""",
  },
]

# ─── BROLL SCHEDULE para los 15 minutos ──────────────────────────────────────
BROLL_SCHEDULE = [
  { "start_time": 15,  "end_time": 35,  "label": "📐 Coordenadas XYZ — Espacio 3D" },
  { "start_time": 60,  "end_time": 80,  "label": "🔢 768 Dimensiones — text-embedding-004" },
  { "start_time": 140, "end_time": 165, "label": "📊 Vector: [0.12, -0.87, 0.34 ... × 768]" },
  { "start_time": 200, "end_time": 225, "label": "📐 Distancia Coseno — Ángulo entre vectores" },
  { "start_time": 280, "end_time": 305, "label": "🎯 Distancia A↔B: 0.04 | A↔C: 0.91" },
  { "start_time": 360, "end_time": 385, "label": "🎙️ Voz: 48,000 muestras/s — Teorema Nyquist" },
  { "start_time": 420, "end_time": 450, "label": "📻 EBU R128 — -14 LUFS Estándar YouTube" },
  { "start_time": 480, "end_time": 510, "label": "🖼️ 1080p = 6,220,800 valores RGB" },
  { "start_time": 560, "end_time": 590, "label": "💾 RAG: 97.66% ahorro | 474KB → 11.5KB" },
  { "start_time": 640, "end_time": 670, "label": "🤖 OpenClaw: AUDITA → vector → acción" },
  { "start_time": 720, "end_time": 750, "label": "🚀 Tu empresa vectorizada en Firestore 768D" },
  { "start_time": 820, "end_time": 860, "label": "⚡ Automatización guiada por geometría" },
]

# ─── SEO TIMESTAMPS para YouTube ─────────────────────────────────────────────
TIMESTAMPS_YOUTUBE = """
00:00 Intro — El Problema: las máquinas no leen
03:00 Las Dimensiones — De 3D a 768D
06:00 Distancia Coseno — Cómo mide la IA el significado
09:00 Voz, Imagen y Video también son vectores
12:00 Aplicación práctica — Por qué cambia tu empresa
14:30 Cierre y próximos pasos
"""

DESCRIPCION_SEO = """
¿Qué es un embedding? ¿Por qué 768 dimensiones?
¿Cómo funciona el RAG que usan las empresas más avanzadas?

En este video explico vectorización desde cero, con geometría real.
Aplica para texto, voz (48kHz EBU R128), imagen (RGB 1080p) y memoria de IA (tokens).

🔧 Stack usado: Google text-embedding-004 | Firestore Vector DB | OpenClaw 2026.7.1
📚 Para fundadores, CEOs y equipos técnicos que quieren entender IA de verdad.

#VectorizacionIA #Embeddings #RAG #InteligenciaArtificial #AutomatizacionEmpresarial
"""

if __name__ == "__main__":
    import json, os, sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    print("=" * 60)
    print(f" {TITULO}")
    print(f" {CANAL} — {VERSION}")
    print("=" * 60)
    print(f" Bloques: {len(GUION)} | Duración total: 15 minutos")
    print(f" B-Roll events: {len(BROLL_SCHEDULE)}")
    print("=" * 60)

    total_chars = sum(len(b["texto"].strip()) for b in GUION)
    total_words = sum(len(b["texto"].split()) for b in GUION)
    print(f"\n📝 Guión: {total_words} palabras | {total_chars} caracteres")
    print(f"🕐 Ritmo: ~{total_words // 15} palabras/minuto (natural conversacional)\n")

    for b in GUION:
        print(f"  Bloque {b['bloque']}: {b['titulo']} ({b['duracion_min']} min)")
        print(f"  B-Roll:  {b['broll_trigger']}\n")

    # Exportar broll_schedule.json para 15 min
    out_dir = r"C:\openclaw\hb-jewelry\public"
    schedule = {
        "version": "2026.7.1",
        "video": "vectorizacion_15min_educativo",
        "total_duration": 900,
        "voice": "Guillermo Real Voice — FM Broadcast 48kHz EBU R128",
        "events": BROLL_SCHEDULE
    }
    schedule_path = os.path.join(out_dir, "broll_schedule_vectorizacion.json")
    with open(schedule_path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, indent=2, ensure_ascii=False)

    # Exportar guion completo como txt para teleprompter
    guion_path = os.path.join(out_dir, "guion_vectorizacion_15min.txt")
    with open(guion_path, "w", encoding="utf-8") as f:
        f.write(f"{TITULO}\n{'='*60}\n\n")
        for b in GUION:
            f.write(f"[BLOQUE {b['bloque']}] {b['titulo'].upper()}\n")
            f.write(f"[B-ROLL: {b['broll_trigger']}]\n")
            f.write(b["texto"].strip())
            f.write("\n\n" + "─"*60 + "\n\n")
        f.write(f"\nYOUTUBE TIMESTAMPS:\n{TIMESTAMPS_YOUTUBE}")
        f.write(f"\nDESCRIPCIÓN SEO:\n{DESCRIPCION_SEO}")

    print(f"\n✅ B-Roll schedule exportado: {schedule_path}")
    print(f"✅ Guión teleprompter: {guion_path}")
    print("\n PRÓXIMO PASO: python generate_real_voice_fm_master.py")
    print(" con GUION = guion_vectorizacion_15min.txt")
