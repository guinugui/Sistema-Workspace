document.addEventListener('DOMContentLoaded', function() {
    // Check if there is a previously active link from local storage
    var activeLinkId = localStorage.getItem('activeLinkId');
    if (activeLinkId) {
        var activeLink = document.getElementById(activeLinkId);
        if (activeLink) {
            var reportUrl = activeLink.getAttribute('data-link');
            loadReport(reportUrl, activeLinkId);
            return;
        }
    }

    // Marcar o primeiro link como ativo ao carregar a página
    var firstLink = document.getElementById('navbar').querySelector('a');
    if (firstLink) {
        var reportUrl = firstLink.getAttribute('data-link');
        var buttonId = firstLink.id;
        loadReport(reportUrl, buttonId);
    }
});

function loadReport(reportUrl, buttonId) {
    console.log(`Carregando relatório: ${reportUrl}`);
    document.getElementById('report-iframe').src = reportUrl;

    // Remover a classe 'active' de todos os links no navbar
    document.querySelectorAll('#navbar a').forEach(btn => btn.classList.remove('active'));

    // Adicionar a classe 'active' ao link clicado
    document.getElementById(buttonId).classList.add('active');

    // Save the active link id to local storage
    localStorage.setItem('activeLinkId', buttonId);
}
// Limpar o localStorage quando a página for fechada ou o navegador for fechado
window.addEventListener('beforeunload', function() {
    localStorage.removeItem('activeLinkId');
});