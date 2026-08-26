# 🧭 MANIFIESTO DE ARQUITECTURA UNIFICADA OPENCLAW 2026
## Estado: Soberano, Estandarizado e Inmutable | Formato Inspirado en DeepSeek Harness

---

## 🎨 Código de Categorías y Jerarquía de Módulos

| Icono | Categoría | Ubicación | Descripción / Rol |
| :---: | :--- | :--- | :--- |
| 🟢 | **Gateway MCP & Pasarela** | [`gateway/`](file:///c:/Users/ipane/openclaw-operativo-2026/gateway) \| [`app.py`](file:///c:/Users/ipane/openclaw-operativo-2026/app.py) | Puntos de entrada HTTP/REST, enrutador MCP, autenticación y Gemini/DeepSeek |
| 🔵 | **Frontend B2B UI** | [`frontend/`](file:///c:/Users/ipane/openclaw-operativo-2026/frontend) | Interfaz React/Vite. Componentes blindados bajo el protocolo `v2.0-stable` |
| 🟡 | **Skills & Plugins** | [`.agents/`](file:///c:/Users/ipane/openclaw-operativo-2026/.agents) | Habilidades especializadas, sub-agentes, plugins y reglas de conducta |
| 🟣 | **Orquestación & DAG** | [`claw-orchestrator/`](file:///c:/Users/ipane/openclaw-operativo-2026/claw-orchestrator) \| [`scripts/`](file:///c:/Users/ipane/openclaw-operativo-2026/scripts) | Grafos CPM, pipelines de cierre, renderizado 1080p y respaldo Rclone |
| 🔴 | **Logs & Telemetría** | [`logs/`](file:///c:/Users/ipane/openclaw-operativo-2026/logs) \| `runtime/logs/` | Registros de auditoría, trazabilidad de inferencia y telemetría de GPU/CPU |
| 🔑 | **Variables de Entorno** | [`.env`](file:///c:/Users/ipane/openclaw-operativo-2026/.env) \| [`.openclaw-master.env`](file:///c:/Users/ipane/.openclaw-master.env) | Fuente Única de Verdad para claves de API (Gemini, DeepSeek, Pickaxe, ElevenLabs) |

---

## 📂 Estructura Detallada del Workspace

```
openclaw-operativo-2026/
├── 🟢 app.py                                # Punto de entrada principal Flask WSGI / Local (8080)
├── 🟢 gateway/                              # Pasarela de microservicios y endpoints MCP
│   ├── app.py                               # Rutas /api/mcp/status, /session, /message, /history
│   └── hb_cotizacion.py                     # Motor de cotizaciones de joyería
├── 🔵 frontend/                             # Aplicación Web React + Vite
│   ├── src/
│   │   ├── components/                      # Componentes UI (Layout, Header, Sidebar, Chat)
│   │   ├── services/                        # Servicios (agentRuntime, eventBus, i18n)
│   │   └── styles/                          # Estilos CSS unificados
├── 🟡 .agents/                              # Gobernanza de Agentes, Habilidades y Plugins
│   ├── AGENTS.md                            # Protocolo de blindaje inmutable v2.0-stable
│   └── skills/                              # Habilidades modulares en SKILL.md
│       ├── digital_human_factory/
│       ├── antigravity-meta-skill-factory-phd/
│       ├── deepseek-harness-orchestrator/
│       └── open-weight-model-hub/
├── 🟣 scripts/                              # Pipelines de automatización y producción
│   ├── pipeline-cierre.ps1                  # Script maestro de cierre (Git + Firebase + Rclone)
│   ├── render_seamless_cosmic_masterpiece_guillermo.py # Motor de video 1080p
│   └── sync-master-env.ps1                  # Sincronizador de API Keys maestro
├── 🟣 claw-orchestrator/                    # Microservicio de orquestación de tareas DAG
├── 🔴 logs/                                 # Logs centralizados de ejecución
├── 🔑 .env                                  # Variables de entorno locales (Sincronizadas)
└── 📦 archive/                              # Repositorio de scripts legacy archivados
```

---

## 🔒 Regla de Oro & Protocolo Antihumo
1. **Un solo lugar para cada responsabilidad**: Queda prohibido duplicar lógica de API o endpoints en archivos temporales sueltos.
2. **Cero archivos `.tmp` flotantes**: Los temporales se procesan en `runtime/` y se eliminan automáticamente tras el pipeline.
3. **Persistencia inmutable**: Sincronización continua en `origin/main` + Google Drive 5TB vía `rclone`.
