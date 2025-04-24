// index.js

document.getElementById('prediction-form').addEventListener('submit', async function (e) {
  e.preventDefault();

  const btn = document.getElementById('predict-button');
  const resultEl = document.getElementById('predicted-count');

  // Disable button & show loading
  btn.textContent = 'Processing…';
  btn.disabled = true;
  resultEl.textContent = '';

  // 1) Gather inputs
  const rawDate = document.getElementById('date').value; // "YYYY-MM-DD"
  const [year, month, day] = rawDate.split('-');
  const date = `${day}/${month}/${year}`;              // "DD/MM/YYYY"

  const hour = parseInt(document.getElementById('hour').value, 10);
  const temperature = parseFloat(document.getElementById('temperature').value);
  const humidity = parseFloat(document.getElementById('humidity').value);
  const wind_speed = parseFloat(document.getElementById('wind-speed').value);
  const visibility = parseFloat(document.getElementById('visibility').value);
  const solar_radiation = parseFloat(document.getElementById('solar-radiation').value);
  const rainfall = parseFloat(document.getElementById('rainfall').value);
  const snowfall = parseFloat(document.getElementById('snowfall').value);
  const seasons = document.getElementById('seasons').value;        // "Spring"/"Summer"/"Autumn"/"Winter"
  const holiday = document.getElementById('holiday').value;        // "No Holiday"/"Holiday"
  const functioning_day = document.getElementById('functioning-day').value; // "Yes"/"No"

  // 2) Build payload
  const payload = {
    date,
    hour,
    temperature,
    humidity,
    wind_speed,
    visibility,
    solar_radiation,
    rainfall,
    snowfall,
    seasons,
    holiday,
    functioning_day
  };

  try {
    // 3) Call your backend
    const resp = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const json = await resp.json();
    if (!resp.ok) throw new Error(json.error || 'Server error');

    // 4) Display prediction
    resultEl.textContent = Math.round(json.prediction);
  } catch (err) {
    console.error('Prediction error:', err);
    resultEl.textContent = 'Error: ' + err.message;
  } finally {
    // 5) Restore button
    btn.textContent = 'Predict Bike Demand';
    btn.disabled = false;
  }
});
