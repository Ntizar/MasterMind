// Shim de comlink para testear workers en Node con esbuild alias.
// Uso: en el test, esbuild({ alias: { comlink: '<ruta>/comlink-shim.mjs' } }).
// Tras importar el bundle del worker, el api expuesto queda en:
//   globalThis.__solmadTestAPI
export function expose(api) {
  globalThis.__solmadTestAPI = api;
}
export function wrap(x) { return x; }
export function proxy(x) { return x; }
export const transfer = () => {};
export const proxyMarker = Symbol('proxyMarker');
