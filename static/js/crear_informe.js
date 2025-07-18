document.addEventListener('DOMContentLoaded', () => {
    const reportForm = document.getElementById('reportForm');
    const reportTypeSelect = document.getElementById('reportType');
    const allReportFields = document.querySelectorAll('.report-fields');
    const formMessage = document.getElementById('formMessage');

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
        }
        // Aquí puedes añadir la lógica para los otros tipos de informe

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