document.addEventListener('DOMContentLoaded', () => {
    const reportForm = document.getElementById('reportForm');
    const reportTypeSelect = document.getElementById('reportType');
    const allReportFields = document.querySelectorAll('.report-fields');
    const formMessage = document.getElementById('formMessage');

    const monitoreoFieldsContainer = document.getElementById('monitoreoFieldsContainer');
    const addMonitoreoFieldBtn = document.getElementById('addMonitoreoField');

    const vulnerabilidadFieldsContainer = document.getElementById('vulnerabilidadFieldsContainer');
    const addVulnerabilidadBtn = document.getElementById('addVulnerabilidad');

    const llamadasContainer = document.getElementById('llamadasContainer');
    const addLlamadaBtn = document.getElementById('addLlamada');

    // Muestra los campos del formulario según el tipo de informe seleccionado
    reportTypeSelect.addEventListener('change', () => {
        const selectedType = reportTypeSelect.value;
        allReportFields.forEach(field => {
            field.style.display = 'none';
        });
        if (selectedType) {
            document.getElementById(`${selectedType}Fields`).style.display = 'block';
        }
    });

    // Lógica para añadir campos de Monitoreo
    addMonitoreoFieldBtn.addEventListener('click', () => {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('form-group');
        fieldGroup.innerHTML = `
            <label>Detalle de Monitoreo:</label>
            <input type="text" placeholder="Tipo de Amenaza" class="monitoreo-amenaza" required>
            <input type="number" placeholder="Valor" class="monitoreo-valor" required>
        `;
        monitoreoFieldsContainer.appendChild(fieldGroup);
    });

    // Lógica para añadir campos de Vulnerabilidad
    addVulnerabilidadBtn.addEventListener('click', () => {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('vulnerabilidad-item');
        fieldGroup.innerHTML = `
            <hr>
            <div class="form-group">
                <label>Nombre de la Vulnerabilidad:</label>
                <input type="text" class="vulnerabilidad-nombre" required>
            </div>
            <div class="form-group">
                <label>Nivel de Criticidad:</label>
                <select class="vulnerabilidad-criticidad" required>
                    <option value="Baja">Baja</option>
                    <option value="Media">Media</option>
                    <option value="Alta">Alta</option>
                    <option value="Crítica">Crítica</option>
                </select>
            </div>
            <div class="form-group">
                <label>Sitio Web:</label>
                <input type="text" class="vulnerabilidad-sitio" required>
            </div>
            <div class="form-group">
                <label>Descripción:</label>
                <textarea class="vulnerabilidad-descripcion" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label>Impacto:</label>
                <textarea class="vulnerabilidad-impacto" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label>Mitigación:</label>
                <textarea class="vulnerabilidad-mitigacion" rows="3" required></textarea>
            </div>
        `;
        vulnerabilidadFieldsContainer.appendChild(fieldGroup);
    });

    // Lógica para añadir campos de Cadena de Llamadas
    addLlamadaBtn.addEventListener('click', () => {
        const fieldGroup = document.createElement('div');
        fieldGroup.classList.add('llamada-item');
        fieldGroup.innerHTML = `
            <hr>
            <div class="form-group">
                <label>Fecha y Hora:</label>
                <input type="datetime-local" class="llamada-fecha" required>
            </div>
            <div class="form-group">
                <label>Persona Contactada:</label>
                <input type="text" class="llamada-persona" required>
            </div>
            <div class="form-group">
                <label>Área:</label>
                <input type="text" class="llamada-area" required>
            </div>
            <div class="form-group">
                <label>Acción:</label>
                <input type="text" class="llamada-accion" required>
            </div>
            <div class="form-group">
                <label>Detalles:</label>
                <textarea class="llamada-detalles" rows="3" required></textarea>
            </div>
        `;
        llamadasContainer.appendChild(fieldGroup);
    });

    reportForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reportType = reportTypeSelect.value;
        const reportTitle = document.getElementById('reportTitle').value;
        let reportData = {
            titulo: reportTitle,
            tipo_informe: reportType
        };

        if (reportType === 'boletin') {
            reportData.contenido = document.getElementById('boletinContent').value;
        } else if (reportType === 'monitoreo') {
            const detalles = [];
            document.querySelectorAll('.monitoreo-amenaza').forEach((input, index) => {
                detalles.push({
                    tipo_amenaza: input.value,
                    valor: parseInt(document.querySelectorAll('.monitoreo-valor')[index].value)
                });
            });
            reportData.detalles = detalles;
        } else if (reportType === 'vulnerabilidad') {
            const vulnerabilidades = [];
            document.querySelectorAll('.vulnerabilidad-item').forEach(item => {
                vulnerabilidades.push({
                    nombre_vulnerabilidad: item.querySelector('.vulnerabilidad-nombre').value,
                    nivel_criticidad: item.querySelector('.vulnerabilidad-criticidad').value,
                    sitio_web: item.querySelector('.vulnerabilidad-sitio').value,
                    descripcion: item.querySelector('.vulnerabilidad-descripcion').value,
                    impacto: item.querySelector('.vulnerabilidad-impacto').value,
                    mitigacion: item.querySelector('.vulnerabilidad-mitigacion').value
                });
            });
            reportData.vulnerabilidades = vulnerabilidades;
        } else if (reportType === 'incidente') {
            const llamadas = [];
            document.querySelectorAll('.llamada-item').forEach(item => {
                llamadas.push({
                    fecha: item.querySelector('.llamada-fecha').value.replace('T', ' '),
                    persona_contacto: item.querySelector('.llamada-persona').value,
                    area_contacto: item.querySelector('.llamada-area').value,
                    accion_comunicacion: item.querySelector('.llamada-accion').value,
                    detalles_comunicacion: item.querySelector('.llamada-detalles').value,
                });
            });

            reportData.incidente = {
                asunto: document.getElementById('asuntoIncidente').value,
                fecha_apertura: document.getElementById('fechaApertura').value.replace('T', ' '),
                fecha_cierre: document.getElementById('fechaCierre').value.replace('T', ' '),
                origen: document.getElementById('origenIncidente').value,
                detalles: document.getElementById('detallesIncidente').value,
                acciones_tomadas: document.getElementById('accionesIncidente').value,
                estado: document.getElementById('estadoIncidente').value,
                criticidad: document.getElementById('criticidadIncidente').value,
                prioridad: document.getElementById('prioridadIncidente').value,
                sitio_afectado: document.getElementById('sitioAfectado').value,
                ip_origen: document.getElementById('ipOrigen').value,
                usuario_responsable_id: parseInt(document.getElementById('usuarioResponsable').value),
                analista_responsable_id: parseInt(document.getElementById('analistaResponsable').value),
                cadena_llamadas: llamadas
            };
        }

        const response = await fetch('http://127.0.0.1:5000/informes/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reportData)
        });

        const data = await response.json();
        if (response.ok) {
            formMessage.style.color = 'green';
            formMessage.textContent = data.message;
            reportForm.reset();
        } else {
            formMessage.style.color = 'red';
            formMessage.textContent = data.error;
        }
    });
});