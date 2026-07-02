# PROTOCOLO DE BLINDAJE PERMANENTE — OpenClaw Cloud 2026

## Estado estable verificado
- **Tag de referencia:** `v2.0-stable`
- **Commit:** `49c8425` — Layout + Header + Sidebar agrupado + estilos unificados
- **Build:** Vite — 198 modulos compilados sin errores

---

## Archivos CRITICOS — PROHIBIDO modificar sin autorizacion explicita del usuario

Los siguientes archivos estan BLINDADOS. Cualquier agente debe tratarlos como de solo lectura
a menos que el usuario diga explicitamente "autorizo cambio en [archivo]":

- frontend/src/components/Layout/Layout.jsx        [BLINDADO]
- frontend/src/components/Header/Header.jsx        [BLINDADO]
- frontend/src/components/Sidebar/Sidebar.jsx      [BLINDADO]
- frontend/src/styles/layout.css                   [BLINDADO]
- frontend/src/styles/sidebar.css                  [BLINDADO]

---

## Reglas de conducta para TODOS los agentes

1. NUNCA sobrescribir archivos criticos con codigo experimental o generico.
2. SIEMPRE verificar que "npm run build" pase antes de cualquier commit a archivos criticos.
3. Si un archivo critico se rompe -> restaurar inmediatamente con:
      git checkout v2.0-stable -- <archivo>
4. Codigo experimental va en ramas temporales (feature/*, exp/*), NUNCA directo a main.
5. Si aparecen archivos basura (.txt con codigo, archivos sin extension) -> eliminar y agregar a .gitignore.
6. Si hay duda entre modificar y proteger -> SIEMPRE PROTEGER.

---

## Protocolo de recuperacion de emergencia

Si el sidebar, header o layout aparecen rotos o vacios, ejecutar en PowerShell:

  git checkout v2.0-stable -- frontend/src/components/Layout/Layout.jsx
  git checkout v2.0-stable -- frontend/src/components/Header/Header.jsx
  git checkout v2.0-stable -- frontend/src/components/Sidebar/Sidebar.jsx
  git checkout v2.0-stable -- frontend/src/styles/layout.css
  git checkout v2.0-stable -- frontend/src/styles/sidebar.css
  cd frontend && npm run build

---

## Arquitectura del frontend (NO cambiar sin protocolo)

App.jsx
  Layout (activeSection, onSelect)
    Header        -> .app-header, .header-brand, .status-dot
    Sidebar       -> 4 grupos: Principal / Operaciones / Marketing & Analytics / Sistema
    <main>        -> contenido por seccion (Dashboard, Chat, Ventas, etc.)

CSS responsable:
  - Layout:  frontend/src/styles/layout.css
  - Sidebar: frontend/src/styles/sidebar.css

---

## Verificacion diaria de integridad

  cd C:\Users\ipane\openclaw-cloud-2026\frontend
  npm run build
  # Debe decir: "built in Xms" sin errores

---

REGLA DE ORO: v2.0-stable es el estado maestro. En caso de duda -> PROTEGER.
