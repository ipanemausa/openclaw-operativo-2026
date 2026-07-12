const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = 'C:\\\\Users\\\\ipane\\\\openclaw-cloud-2026';
const FRONTEND = path.join(PROJECT_ROOT, 'frontend');

const COMPONENTS = [
  'Productos','Ventas','Clientes','Ordenes','Reportes',
  'Inventario','Proveedores','Pagos','Configuracion','Ayuda'
];

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function backup(file) {
  if (!fs.existsSync(file)) return;
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  fs.copyFileSync(file, file + '.bak_' + stamp);
}

function componentSource(name) {
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

function main() {
  const srcDir = path.join(FRONTEND, 'src');
  const compDir = path.join(srcDir, 'components');

  ensureDir(compDir);

  COMPONENTS.forEach(name => {
    const file = path.join(compDir, name + '.tsx');
    backup(file);
    fs.writeFileSync(file, componentSource(name));
    console.log('✔ Componente generado:', name);
  });

  console.log('\\n✔ CAMIN VITE completado.');
}

main();
