# ═══════════════════════════════════════════════════════════════
# OpenClaw Cloud 2026 - GUÍA PASO A PASO VISUAL
# ¿DÓNDE COLOCAR LA API KEY DE PICKAXE?
# ═══════════════════════════════════════════════════════════════

## 📋 RESUMEN VISUAL

```
┌─────────────────────────────────────────────────────────┐
│  ARCHIVO: .env                                          │
│  LÍNEA: ~24                                             │
│                                                         │
│  BUSCA ESTO:                                            │
│  PICKAXE_API_KEY=pk-your-api-key-from-pickaxe-dot-ai   │
│                  ▲                                      │
│                  │                                      │
│              REEMPLAZA ESTO POR TU CLAVE               │
│                  │                                      │
│                  ▼                                      │
│  REEMPLAZA CON:                                         │
│  PICKAXE_API_KEY=pk-abc123def456ghi789jkl              │
│                  ▲                                      │
│                  │                                      │
│            Tu clave real de Pickaxe                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📍 LOCALIZACIÓN EXACTA

**Archivo:** `C:\Users\ipane\openclaw-cloud-2026\.env`

**Línea número:** Busca la línea que dice `PICKAXE_API_KEY=`

**Sección:** Está bajo el encabezado:
```
# ═══════════════════════════════════════════════════════════════
# 🔑 PICKAXE LLM - MOTOR PRINCIPAL (OBLIGATORIO)
# ═══════════════════════════════════════════════════════════════
```

---

## 🔑 PASO A PASO: OBTENER LA API KEY

### PASO 1: Ve a Pickaxe.ai
```
1. Abre tu navegador
2. Ve a: https://pickaxe.ai
3. Haz clic en "Sign Up" o "Register"
```

### PASO 2: Crea una cuenta (es GRATIS)
```
1. Usa tu email
2. Crea una contraseña
3. Confirma tu email
```

### PASO 3: Obtén tu API Key
```
1. Inicia sesión en Pickaxe
2. Ve a: Settings → API Keys (o Account)
3. Haz clic en "Create API Key" o "Generate Key"
4. Copia la clave completa (empieza con "pk-")
5. Guárdalo en un lugar seguro
```

---

## 🔴 PASO A PASO: ACTUALIZAR EL .env

### OPCIÓN A: Usando un editor de texto (Windows)

```
1. Abre el Explorador de archivos
2. Navega a: C:\Users\ipane\openclaw-cloud-2026\
3. Haz clic derecho en el archivo ".env"
4. Selecciona: "Abrir con" → "Bloc de notas"
5. Presiona Ctrl+F para buscar
6. Busca: "pk-your-api-key-from-pickaxe-dot-ai"
7. Reemplaza completamente esta línea con:
   PICKAXE_API_KEY=pk-tu-clave-aqui
   (ej: PICKAXE_API_KEY=pk-abc123def456ghi789jkl)
8. Presiona Ctrl+S para guardar
9. Cierra el archivo
```

### OPCIÓN B: Usando PowerShell (recomendado)

```powershell
# Abre PowerShell como administrador
# Navega al directorio:
cd C:\Users\ipane\openclaw-cloud-2026

# Edita el archivo con Notepad:
notepad .env

# En Notepad:
# 1. Presiona Ctrl+F
# 2. Busca: pk-your-api-key-from-pickaxe-dot-ai
# 3. Reemplaza con tu clave: pk-tu-clave-real
# 4. Presiona Ctrl+S para guardar
# 5. Cierra Notepad
```

### OPCIÓN C: Usando nano (si tienes Git Bash o WSL)

```bash
cd C:\Users\ipane\openclaw-cloud-2026
nano .env

# En nano:
# 1. Presiona Ctrl+W para buscar
# 2. Busca: pk-your-api-key
# 3. Edita la línea: PICKAXE_API_KEY=pk-tu-clave-real
# 4. Presiona Ctrl+X para salir
# 5. Presiona Y para confirmar guardar
# 6. Presiona Enter para el nombre del archivo
```

---

## ⚠️ VERIFICACIÓN - ANTES DE DESPLEGAR

Después de editar, verifica que:

```
✓ La línea PICKAXE_API_KEY tiene tu clave (empieza con pk-)
✓ NO está en blanco
✓ NO tiene "pk-your-api-key-from-pickaxe-dot-ai"
✓ También cambiaste:
  - DB_PASSWORD (contraseña BD)
  - REDIS_PASSWORD (contraseña Redis)
  - QDRANT_API_KEY (API de Qdrant)
  - SECRET_KEY (key secreto Flask)
```

---

## 🔐 VALORES SEGUROS A USAR (COPIA Y PEGA)

Si no quieres generar los tuyos, puedes usar estos como ejemplo:
(⚠️ Cambia esto en producción real)

```
DB_PASSWORD=SecureDB2026!@#Xyz123
REDIS_PASSWORD=SecureRedis2026!@#Abc456
QDRANT_API_KEY=SecureQdrant2026!@#Def789
SECRET_KEY=SuperSecretFlaskKey2026!@#GhiJkl123MnoPqr456
```

---

## ✅ LÍNEA EXACTA A CAMBIAR

**BUSCA ESTO (línea ~24):**
```
PICKAXE_API_KEY=pk-your-api-key-from-pickaxe-dot-ai
```

**REEMPLAZA CON (TU CLAVE REAL):**
```
PICKAXE_API_KEY=pk-abc123def456ghi789jklmnopqrst
```

---

## 🚀 DESPUÉS DE GUARDAR

Una vez que actualizaste el `.env`:

```bash
# 1. Abre PowerShell
# 2. Navega al proyecto:
cd C:\Users\ipane\openclaw-cloud-2026

# 3. Despliega (esto construye y inicia todos los servicios):
docker-compose up -d --build

# 4. Espera 30 segundos mientras los servicios inician
# 5. Verifica que todo funciona:
curl http://localhost:8080/health

# 6. Accede a OpenClaw:
# http://localhost (en tu navegador)
```

---

## 🆘 SI ALGO SALE MAL

```bash
# Ver logs del error:
docker-compose logs openclaw_app

# Revisar que .env está correcto:
cat .env | findstr "PICKAXE_API_KEY"

# Reintentar:
docker-compose down
docker-compose up -d --build
```

---

## 📝 CHECKLIST FINAL

```
☐ Copié la API key de Pickaxe.ai (empieza con pk-)
☐ Abrí el archivo .env en un editor
☐ Encontré la línea PICKAXE_API_KEY=pk-your-api-key-from-pickaxe-dot-ai
☐ Reemplacé TODA la línea con mi clave real
☐ También cambié DB_PASSWORD, REDIS_PASSWORD, QDRANT_API_KEY, SECRET_KEY
☐ Guardé el archivo (.env)
☐ Ejecuté: docker-compose up -d --build
☐ Esperé 30 segundos
☐ Ejecuté: curl http://localhost:8080/health
☐ Accedí a http://localhost en el navegador
```

---

## 🎯 LÍNEA VISUAL CON FLECHAS

```
Archivo: C:\Users\ipane\openclaw-cloud-2026\.env
         ↓
Busca:   PICKAXE_API_KEY=pk-your-api-key-from-pickaxe-dot-ai
         ↓
Borra:   pk-your-api-key-from-pickaxe-dot-ai
         ↓
Escribe: pk-abc123def456ghi789jklmnopqrst
         ↓
Guarda:  Ctrl+S
         ↓
Listo:   docker-compose up -d --build
```

---

¡Eso es todo! No es complicado. Solo busca, reemplaza y guarda.
