// Função para abrir o modal de edição com os dados preenchidos
function openEditModal(id, nome, descricao, imagem, sequencia, cor) {
    var modal = document.getElementById('editModal');
    modal.style.display = 'block';

    // Preencher os campos do formulário de edição
    document.getElementById('editID').value = id;
    document.getElementById('editIDDisplay').textContent = id;
    document.getElementById('editNome').value = nome;
    document.getElementById('editDescricao').value = descricao;
    document.getElementById('editImagem').value = imagem;
    document.getElementById('editSequencia').value = sequencia;
    document.getElementById('editCor').value = cor;
}

// Função para fechar o modal de edição
function closeEditModal() {
    var modal = document.getElementById('editModal');
    modal.style.display = 'none';
}

// Função para fechar o modal de adição
function closeAddModal() {
    var modal = document.getElementById('myModal');
    modal.style.display = 'none';
}

// Fechar o modal quando o usuário clica no botão de fechar
var closeButtons = document.querySelectorAll('.close');
closeButtons.forEach(function(button) {
    button.addEventListener('click', function() {
        var modal = button.closest('.modal');
        modal.style.display = 'none';
    });
});
