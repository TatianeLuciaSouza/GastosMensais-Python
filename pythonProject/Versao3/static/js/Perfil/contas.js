//Alterar conta - Início
document.querySelectorAll('#pContasBody .alt').forEach(cell => {
    cell.addEventListener('click', function() {
        const originalText = cell.textContent;
        const input = document.createElement('input');
        input.value = originalText;
        cell.innerHTML = ''; // Limpa o conteúdo da célula
        cell.appendChild(input);
        const coluna = cell.cellIndex;
        input.focus();
        const row = cell.closest('tr');
        const idTabela = row.querySelector('td:last-child').textContent;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const valor = input.value;
                const tipo = 1;
                cell.textContent = valor;

                // Envie a atualização para o servidor
                fetch('/alterar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: idTabela,
                        valor: valor,
                        coluna: coluna,
                        tipo: tipo
                    }) // Passa também a coluna editada
                })

                .then(response => {
                    if (response.status === 200) {
                        console.log('aqui');
                        carregaGrid();
                    } else {
                        console.error('Erro ao atualizar:', data.error);
                        cell.textContent = originalText; // Reverte se falhar
                    }
                });
            }
        });

        input.addEventListener('blur', () => {
            cell.textContent = originalText; // Reverte se sair do campo
        });
    });
});
//Alterar Conta - Fim

//Excluir Conta - Início
document.getElementById('btnExcluir').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll("input[type=checkbox]");

    // Array para armazenar os IDs dos checkboxes selecionados
    const idsToDelete = [];

    // Itera sobre todos os checkboxes
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) { // Verifica se o checkbox está marcado
            idsToDelete.push(checkbox.value); // Adiciona o valor ao array
        }
    });
    console.log(idsToDelete);
    if (idsToDelete.length === 0) {
        return alert('Nenhum item selecionado para exclusão.');
    }

    fetch('/deletar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idTabela: idsToDelete, tipo: 4 }),
    })
     .then(response => {
        if (response.status === 200) {
            // Se o status for 204, a exclusão foi bem-sucedida
            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    checkbox.closest('tr').remove(); // Remove as linhas correspondentes
                }
            });
            alert('Itens excluídos com sucesso!');
        } else {
            // Se não for 204, trata como erro
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao excluir itens: ' + error.message);
    });
});
//Excluir Conta - Fim

//Carregar Tela - Início
function carregaGrid() {
    const tbody = document.getElementById('pContasBody');
    if (!tbody) {
        console.error('pContasBody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/pContas?tipo=${encodeURIComponent('JS')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData => {
            tbody.innerHTML = ''; // Limpa o conteúdo atual

            // Verifica a estrutura da resposta
            if (responseData && Array.isArray(responseData.dados) && responseData.dados.length > 0) {
                responseData.dados.forEach(contas => { // Correção aqui
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td >${contas.conta}</td>
                        <td>${contas.tpConta}</td>
                        <td class="editable" data-col="parcela">${contas.parcela}</td>
                        <td class="editable" data-col="desc">${contas.desc}</td>
                        <td class="editable" data-col="vlTotal">${contas.vlTotal}</td>
                        <td>${contas.vlParcela}</td>
                        <td><input type="checkbox" value="${contas.ID}"></td>
                        <td style="display: none;">${contas.ID}</td>
                    `;
                    tbody.appendChild(row);
                });
               colunasEditaveis(); //Torna as células editáveis
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="8">Nenhuma conta encontrada.</td>'; // Corrigido o colspan
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error.message)); // Mensagem de erro mais descritiva
}
function colunasEditaveis() {
    const editableCells = document.querySelectorAll('#pContasBody .editable');

    editableCells.forEach(cell => {
        cell.addEventListener('click', function() {
        const originalText = cell.textContent;
        const input = document.createElement('input');
        input.value = originalText;
        cell.innerHTML = ''; // Limpa o conteúdo da célula
        cell.appendChild(input);
        const coluna = cell.cellIndex;
        input.focus();
        const row = cell.closest('tr');
        const idTabela = row.querySelector('td:last-child').textContent;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const valor = input.value;
                const tipo = 1;
                cell.textContent = valor;

                // Envie a atualização para o servidor
                fetch('/alterar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: idTabela,
                        valor: valor,
                        coluna: coluna,
                        tipo: tipo
                    }) // Passa também a coluna editada
                })

                .then(response => {
                    if (response.status === 200) {
                        carregaGrid();
                    } else {
                        console.error('Erro ao atualizar:', data.error);
                        cell.textContent = originalText; // Reverte se falhar
                    }
                });
            }
        });

        input.addEventListener('blur', () => {
            cell.textContent = originalText; // Reverte se sair do campo
        });
    });
    });
}
//Carregar Tela - Fim