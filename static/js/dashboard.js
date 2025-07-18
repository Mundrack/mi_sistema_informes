document.addEventListener('DOMContentLoaded', () => {
    const reportsContainer = document.getElementById('reportsContainer');
    const metricContainer = document.getElementById('metricContainer');
    const filterInput = document.getElementById('filterInput');
    const filterButton = document.getElementById('filterButton');
    const clearFilterButton = document.getElementById('clearFilterButton');
    const deletedButton = document.getElementById('deletedButton');
    const loadingMessage = document.getElementById('loadingMessage');
    
    const API_URL = 'http://127.0.0.1:5000/informes';
    const API_METRICS_URL = 'http://127.0.0.1:5000/dashboard/metrics';

    // Función para obtener y mostrar métricas
    const fetchMetrics = async () => {
        try {
            const response = await fetch(API_METRICS_URL);
            const metrics = await response.json();
            displayMetrics(metrics);
        } catch (error) {
            console.error('Error al cargar las métricas:', error);
        }
    };

    // Función para mostrar las métricas en cuadros
    const displayMetrics = (metrics) => {
        metricContainer.innerHTML = `
            <div class="metric-card" data-report-type="monitoreo">
                <h3>Informes de Monitoreo</h3>
                <p>${metrics.total_monitoreo}</p>
            </div>
            <div class="metric-card" data-report-type="vulnerabilidad">
                <h3>Informes de Vulnerabilidad</h3>
                <p>${metrics.total_vulnerabilidad}</p>
            </div>
            <div class="metric-card" data-report-type="incidente">
                <h3>Informes de Incidente</h3>
                <p>${metrics.total_incidente}</p>
            </div>
            <div class="metric-card" data-report-type="boletin">
                <h3>Boletines</h3>
                <p>${metrics.total_boletin}</p>
            </div>
            <div class="metric-card" data-report-type="total">
                <h3>Total de Informes</h3>
                <p>${metrics.total_informes}</p>
            </div>
        `;

        // Añadir lógica para que los cuadros sean clicables
        document.querySelectorAll('.metric-card').forEach(card => {
            card.addEventListener('click', () => {
                const reportType = card.dataset.reportType;
                if (reportType === 'total') {
                    fetchReports(); // Mostrar todos los informes
                } else {
                    fetchReports(reportType); // Filtrar por tipo
                    filterInput.value = reportType;
                }
            });
        });
    };

    // Función para obtener y mostrar informes
    const fetchReports = async (filter = null, showDeleted = false) => {
        reportsContainer.innerHTML = '';
        loadingMessage.style.display = 'block';

        let url = API_URL;
        let params = new URLSearchParams();
        
        if (filter) {
            params.append('tipo_informe', filter);
        }
        
        if (showDeleted) {
            params.append('incluir_eliminados', 'true');
        }
        
        url += '?' + params.toString();

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Error ${response.status}: ${response.statusText}`);
            }
            const reports = await response.json();
            displayReports(reports);
        } catch (error) {
            reportsContainer.innerHTML = `<p class="error-message">Error: ${error.message}. Por favor, asegúrate de que el servidor está corriendo.</p>`;
        } finally {
            loadingMessage.style.display = 'none';
        }
    };

    const displayReports = (reports) => {
        if (reports.length === 0) {
            reportsContainer.innerHTML = '<p class="no-reports">No se encontraron informes.</p>';
            return;
        }

        reports.forEach(report => {
            const reportCard = document.createElement('div');
            reportCard.classList.add('report-card');
            
            const date = new Date(report.fecha_creacion).toLocaleDateString('es-ES');
            
            reportCard.innerHTML = `
                <h3>${report.titulo}</h3>
                <p><strong>Tipo:</strong> ${report.tipo_informe}</p>
                <p><strong>Autor:</strong> ${report.autor_nombre}</p>
                <p class="report-meta">Fecha: ${date}</p>
            `;
            reportsContainer.appendChild(reportCard);
        });
    };

    // Event listeners para los botones
    filterButton.addEventListener('click', () => {
        const filterValue = filterInput.value.trim().toLowerCase();
        fetchReports(filterValue);
    });

    clearFilterButton.addEventListener('click', () => {
        filterInput.value = '';
        fetchReports();
    });

    deletedButton.addEventListener('click', () => {
        fetchReports(null, true);
    });

    // Cargar métricas e informes al iniciar la página
    fetchMetrics();
    fetchReports();
});