# CLI Reference

## Comandos

### `raspal fetch <url>`
Scrapea una URL y muestra el contenido.
- `--engine` (scrapling, playwright, stealth, auto)
- `--extract` extrae con IA
- `--output` guarda a archivo
- `--no-cache` ignora cache
- `--verbose` modo detallado

### `raspal run <config.yaml>`
Ejecuta un pipeline YAML.

### `raspal async-fetch <url>`
Fetch asincrono.

### `raspal async-batch <urls>...`
Fetch asincrono multiple.

### `raspal queue <config.yaml>`
Ejecuta con cola de persistencia SQLite.
- `--db` ruta de base de datos
- `-o` archivo de salida

### `raspal compliance <url>`
Verifica robots.txt y dominio sensible.

### `raspal validate <config.yaml>`
Valida sintaxis de pipeline YAML.

### `raspal status`
Muestra estado del sistema (cache, Ollama, version).

### `raspal setup`
Prepara el entorno (instala browsers, verifica Ollama).

### `raspal init`
Scaffold de proyecto con estructura de directorios.

### `raspal report`
Genera reporte HTML desde resultados JSON.
- `--input` archivo JSON de entrada
- `--output` archivo HTML de salida

### `raspal serve`
Inicia dashboard web en http://localhost:8462.

### `raspal clear-cache`
Limpia cache de fetch.

### `raspal demo`
Scrapea httpbin.org/html como demostracion.

### `raspal version`
Muestra la version instalada.

## Flags globales

- `--help` ayuda del comando
- `--verbose` salida detallada
