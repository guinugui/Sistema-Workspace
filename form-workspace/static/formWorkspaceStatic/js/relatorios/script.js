// Função para abrir o modal de adição de relatório
function openAddModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
}

// Função para fechar o modal de adição de relatório
function closeAddModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
}


// Fechar o modal quando o usuário clica no botão de fechar
var closeButtons = document.querySelectorAll('.close');
closeButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        var modal = button.closest('.modal');
        modal.style.display = 'none';
    });
});

function confirmDelete(id_relatorio, workspace_id) {
    var confirmMsg = "Tem certeza que deseja deletar?";
    if (confirm(confirmMsg)) {
        openDeleteModal(id_relatorio, workspace_id);
        return true;
    } else {
        return false;
    }
}

function openDeleteModal(id_relatorio, id_workspace) {
    document.getElementById('deleteIDWorkspace').value = id_workspace;
    document.getElementById('deleteForm').action = '/main/relatorios/delete/' + id_relatorio;
    document.getElementById('deleteForm').submit(); // Envie o formulário de deleção
}