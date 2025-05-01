// 💬 Esperar a que cargue todo el DOM
document.addEventListener('DOMContentLoaded', () => {
    // 🎯 Obtener el formulario
    const form = document.getElementById('predictForm');
    const resultadoDiv = document.getElementById('resultado');

    // 🎯 Escuchar el submit del formulario
    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Evitar recargar la página

        // 📝 Capturar los valores ingresados
        const obp_diff = parseFloat(document.getElementById('obp_diff').value);
        const slg_diff = parseFloat(document.getElementById('slg_diff').value);
        const woba_diff = parseFloat(document.getElementById('woba_diff').value);
        const era_diff = parseFloat(document.getElementById('era_diff').value);
        const fip_diff = parseFloat(document.getElementById('fip_diff').value);

        // 📦 Crear el JSON para enviar
        const data = {
            obp_diff,
            slg_diff,
            woba_diff,
            era_diff,
            fip_diff
        };

        try {
            // 🔥 Enviar el POST a nuestro endpoint /predict
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                // 🎯 Mostrar el resultado de la predicción
                resultadoDiv.style.display = 'block';
                resultadoDiv.innerHTML = `
                    🏆 <b>Equipo Ganador Probable:</b> ${result.equipo_ganador_probable}<br>
                    ⚾ <b>Diferencial Estimado:</b> ${result.diferencial_carreras_estimado}<br>
                    🔵 <b>Probabilidad Local:</b> ${result.probabilidad_ganador_local * 100}%<br>
                    🔴 <b>Probabilidad Visitante:</b> ${result.probabilidad_ganador_visitante * 100}%
                `;
            } else {
                // ⚠️ Mostrar error
                resultadoDiv.style.display = 'block';
                resultadoDiv.innerHTML = `❌ Error: ${result.error}`;
            }
        } catch (error) {
            // ⚠️ Error de conexión
            resultadoDiv.style.display = 'block';
            resultadoDiv.innerHTML = `❌ Error de conexión: ${error.message}`;
        }
    });
});
