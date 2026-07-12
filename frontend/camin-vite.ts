import * as fs from "fs";
import * as path from "path";

type ComponentSpec = {
  name: string;
  filename: string;
  subdir: string;
};

const PROJECT_ROOT = "C:\\Users\\ipane\\openclaw-cloud-2026";
const FRONTEND_CANDIDATES = ["frontend"];

const COMPONENTS: ComponentSpec[] = [
  { name: "Productos", filename: "Productos.tsx", subdir: "components" },
  { name: "Ventas", filename: "Ventas.tsx", subdir: "components" },
  { name: "Clientes", filename: "Clientes.tsx", subdir: "components" },
  { name: "Ordenes", filename: "Ordenes.tsx", subdir: "components" },
  { name: "Reportes", filename: "Reportes.tsx", subdir: "components" },
  { name: "Inventario", filename: "Inventario.tsx", subdir: "components" },
  { name: "Proveedores", filename: "Proveedores.tsx", subdir: "components" },
  { name: "Pagos", filename: "Pagos.tsx", subdir: "components" },
  { name: "Configuracion", filename: "Configuracion.tsx", subdir: "components" },
  { name: "Ayuda", filename: "Ayuda.tsx", subdir: "components" },
];

function log(msg: string) {
  process.stdout.write(msg + "\n");
}

function detectFrontendRoot(): string {
  for (const candidate of FRONTEND_CANDIDATES) {
    const full = path.join(PROJECT_ROOT, candidate);
    if (!fs.existsSync(full)) continue;

    const pkg = path.join(full, "package.json");
    const src = path.join(full, "src");

    if (fs.existsSync(pkg) && fs.existsSync(src)) {
      return full;
    }
  }
  throw new Error("No se encontró frontend.");
}

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function backup(file: string) {
  if (!fs.existsSync(file)) return;
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  fs.copyFileSync(file, file + ".bak_" + stamp);
}

function componentSource(name: string): string {
  return \import React from "react";

export const \ = () => {
  return (
    <div style={{ padding: "1rem" }}>
      <h2>\</h2>
      <p>Componente base generado automáticamente.</p>
    </div>
  );
};

export default \;
\;
}

function writeComponent(root: string, spec: ComponentSpec) {
  const dir = path.join(root, "src", spec.subdir);
  ensureDir(dir);

  const file = path.join(dir, spec.filename);
  backup(file);

  fs.writeFileSync(file, componentSource(spec.name));
}

function main() {
  const root = detectFrontendRoot();
  for (const c of COMPONENTS) writeComponent(root, c);
  log("✔ CAMIN VITE completado.");
}

main();
