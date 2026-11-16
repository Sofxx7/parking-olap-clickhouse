# OLAP de estacionamientos con ClickHouse

Demo analítica para explorar registros de ocupación por cámara y hora. ClickHouse almacena los eventos en una tabla `MergeTree`; SQL agrupa los registros por dimensiones y una aplicación estática presenta los resultados.

**Demo pública:** https://sofxx7.github.io/parking-olap-clickhouse/

## Datos

El repositorio incluye un CSV **sintético** con el mismo esquema básico de `visualdetection.csv`. Se usa una muestra creada para esta demo y no se redistribuyen el archivo ni las imágenes del laboratorio. Puedes sustituir `data/visualdetection_sample.csv` por una copia local del CSV de la práctica para explorar esos datos.

El porcentaje ocupado en la demo es una proporción de lecturas etiquetadas como ocupadas. No equivale a capacidad física ni a porcentaje del tiempo con espacios ocupados.

## Flujo

1. Inicia un ClickHouse local.
2. `scripts/build_data.py` crea la base y la tabla `MergeTree`.
3. El script carga el CSV y ejecuta dos consultas de agregación.
4. Las respuestas se escriben en `site/data.json`.
5. GitHub Actions repite el proceso con un contenedor ClickHouse y publica el tablero en GitHub Pages al recibir cambios en `main`.

## Ejecución local

Requiere Docker y Python 3.12 o superior.

```powershell
$env:CLICKHOUSE_PASSWORD = "demo-password"
docker run --name clickhouse-olap -d `
  -p 127.0.0.1:8123:8123 `
  -e "CLICKHOUSE_PASSWORD=$env:CLICKHOUSE_PASSWORD" `
  clickhouse/clickhouse-server:26.10.3.7
python scripts/build_data.py
python -m http.server 8000 --directory site
```

La clave `demo-password` sirve únicamente para el contenedor local efímero. Abre `http://localhost:8000`. El script elimina y vuelve a crear la tabla de demostración en cada ejecución para que no duplique las filas.

## Despliegue

El workflow `.github/workflows/deploy.yml` construye los resultados usando ClickHouse en cada push a `main` y los publica mediante GitHub Pages. No necesita credenciales externas.

## Límites del ejemplo

La página publicada presenta agregaciones generadas durante el flujo automatizado; no consulta un servidor ClickHouse público. Para desplegar una base ClickHouse administrada y conectarla a una aplicación en línea se necesitaría configurar un servicio y sus credenciales por separado.

## Referencias

- [MergeTree table engine](https://clickhouse.com/docs/reference/engines/table-engines/mergetree-family/mergetree)
- [CSV and CSVWithNames formats](https://clickhouse.com/docs/reference/formats/CSV/CSV)
- [ClickHouse local development](https://clickhouse.com/docs/get-started/setup/install)
