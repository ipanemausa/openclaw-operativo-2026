# Estado de Restauración Automática (ESTADO_RESTAURACION.md)

## Contexto para el Agente (Antigravity/Claude)

Hola, colega IA. Si acabas de iniciar una nueva sesión tras un "restart", usa este documento para reorientarte instantáneamente.

### 1. Versiones y Ramas
- **Versión de OpenClaw:** 2026.7.1
- **Modelo de Trabajo:** El proyecto está operando bajo una arquitectura *Fullstack Monolítica (Docker Compose + NGINX)*.
- **Entorno:** Free Tier enfocado (DeepSeek, Gemini Live, y computación al borde).

### 2. Logros y Estado Actual
Hemos logrado optimizar la ruta crítica del *Proyecto Portafolio de Entrevistas* de la siguiente manera:
- **Financial RAG Worker:** Integrado en el puerto 8093 y ruteado mediante NGINX en `/api/rag`. Utiliza Qdrant para almacenar embeddings de forma optimizada en memoria.
- **Voice Worker (Entrevistas):** Ruteado vía NGINX en `/ws/voice`. Gemini actúa con un prompt de *Interview Proxy*, con tono corporativo y calmado, traduciendo de español a inglés y viceversa de forma bidireccional en tiempo real.
- **Edge Computing (Avatar Visual):** Se ELIMINÓ la dependencia del microservicio `avatar_hub` (generador de video) porque generaba colas infinitas (lag) en Free Tier. En su lugar, el Frontend (`hb-jewelry/src/components/AvatarMeet/AvatarMeet.jsx`) usa la Web Audio API (AudioContext) para analizar el volumen del stream de audio entrante y animar matemáticamente los labios de un avatar estático mediante CSS (`transform: scale`).

### 3. Tareas Pendientes / Siguientes Pasos
Si el humano pide "continuar donde lo dejamos", revisa estos puntos:
1. **Configuración VPS / Cloud Run:** Desplegar el `docker-compose.yml` en la máquina destino (o ejecutar `npm run build` si van a usar Vercel solo para UI temporalmente).
2. **Personalización del Avatar:** El Avatar visual actualmente usa un placeholder en React. Falta inyectar la imagen real del usuario.
3. **Data Financiera RAG:** Verificar si el usuario ya proporcionó el dataset JSON/CSV del módulo financiero de Muncher/Teso para inyectarlo en Qdrant.

**Nota Operativa:** Si cambias la arquitectura, actualiza el diagrama Mermaid en el `README.md` y luego actualiza este mismo archivo. Al terminar tu bloque de trabajo, ejecuta siempre el script de backup.
