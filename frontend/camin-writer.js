const fs = require("fs");
const path = require("path");

const frontend = "C:\\\\Users\\\\ipane\\\\openclaw-cloud-2026\\\\frontend";
const target = path.join(frontend, "camin-vite.js");

const content = [
"const fs = require('fs');",
"const path = require('path');",
"",
"const PROJECT_ROOT = 'C:\\\\Users\\\\ipane\\\\openclaw-cloud-2026';",
"const FRONTEND = path.join(PROJECT_ROOT, 'frontend');",
"",
"const COMPONENTS = [",
"  'Productos','Ventas','Clientes','Ordenes','Reportes',",
"  'Inventario','Proveedores','Pagos','Configuracion','Ayuda'",
"];",
"",
"function ensureDir(dir) {",
"  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });",
"}",
"",
"function backup(file) {",
"  if (!fs.existsSync(file)) return;",
"  const stamp = new Date().toISOString().replace(/[:.]/g, '-');",
"  fs.copyFileSync(file, file + '.bak_' + stamp);",
"}",
"",
"function componentSource(name) {",
"  return (",
"    'import React from \"react\";\\n\\n' +",
"    'export const ' + name + ' = () => {\\n' +",
"    '  return (\\n' +",
"    '    <div style={{ padding: \"1rem\" }}>\\n' +",
"    '      <h2>' + name + '</h2>\\n' +",
"    '      <p>Componente base generado automáticamente.</p>\\n' +",
"    '    </div>\\n' +",
"    '  );\\n' +",
"    '};\\n\\n' +",
"    'export default ' + name + ';\\n'",
"  );",
"}",
"",
"function main() {",
"  const srcDir = path.join(FRONTEND, 'src');",
"  const compDir = path.join(srcDir, 'components');",
"",
"  ensureDir(compDir);",
"",
"  COMPONENTS.forEach(name => {",
"    const file = path.join(compDir, name + '.tsx');",
"    backup(file);",
"    fs.writeFileSync(file, componentSource(name));",
"    console.log('✔ Componente generado:', name);",
"  });",
"",
"  console.log('\\n✔ CAMIN VITE completado.');",
"}",
"",
"main();"
].join("\n");

fs.writeFileSync(target, content);
console.log("✔ Archivo camin-vite.js generado correctamente.");
