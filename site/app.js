const fmt = new Intl.NumberFormat('es-PE');
const pct = new Intl.NumberFormat('es-PE', { maximumFractionDigits: 2 });
let payload;

function render() {
  const filter = document.querySelector('#camera-filter').value;
  const hourly = payload.by_hour.filter(row => filter === 'all' || row.camera === filter);
  const cameras = payload.by_camera;
  document.querySelector('#total').textContent = fmt.format(payload.totals.total_readings);
  document.querySelector('#occupied').textContent = fmt.format(payload.totals.occupied_readings);
  document.querySelector('#rate').textContent = `${pct.format(payload.totals.occupied_reading_pct)}%`;

  const max = Math.max(...cameras.map(row => row.occupied_readings), 1);
  document.querySelector('#camera-chart').innerHTML = cameras.map(row => `
    <div class="camera-row"><span class="camera-name">${row.camera}</span>
    <div class="bar-track"><div class="bar-fill" style="width:${100 * row.occupied_readings / max}%"></div></div>
    <span class="camera-value">${fmt.format(row.occupied_readings)} / ${pct.format(row.occupied_reading_pct)}%</span></div>`).join('');

  document.querySelector('#hourly-rows').innerHTML = hourly.map(row => `
    <tr><td>${row.year}-${String(row.month).padStart(2, '0')}</td><td>${row.camera}</td>
    <td>${String(row.hour).padStart(2, '0')}:00</td><td>${fmt.format(row.total_readings)}</td>
    <td>${fmt.format(row.occupied_readings)}</td><td>${pct.format(row.occupied_reading_pct)}%</td></tr>`).join('') || '<tr><td colspan="6">No hay registros.</td></tr>';
}

fetch('data.json')
  .then(response => { if (!response.ok) throw new Error('No se pudo cargar data.json'); return response.json(); })
  .then(data => {
    payload = data;
    const select = document.querySelector('#camera-filter');
    for (const row of payload.by_camera) {
      const option = document.createElement('option');
      option.value = row.camera;
      option.textContent = `Cámara ${row.camera}`;
      select.append(option);
    }
    render();
  })
  .catch(error => { document.querySelector('#status').textContent = `${error.message}. Ejecuta el flujo automatizado antes de abrir el tablero.`; });

document.querySelector('#camera-filter').addEventListener('change', () => payload && render());
