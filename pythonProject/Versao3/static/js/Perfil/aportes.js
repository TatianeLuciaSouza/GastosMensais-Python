const checkboxes = document.querySelectorAll('input[name="opcao"]');

// Adiciona um evento de click a cada checkbox
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function(event) {
        const value = event.target.value; // Captura o valor do checkbox clicado
        carregaGrid(value);
    });
});

//Alterar conta - Início
document.querySelectorAll('#pAportesBody .alt').forEach(cell => {
    cell.addEventListener('click', function() {
        const originalText = cell.textContent;
        const input = document.createElement('input');
        input.value = originalText;
        cell.innerHTML = ''; // Limpa o conteúdo da célula
        cell.appendChild(input);
        const coluna = cell.cellIndex;
        input.focus();
        const row = cell.closest('tr');
        const idTabela = row.querySelectorAll('td')[0].textContent;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const valor = input.value;
                const tipo = 3;
                cell.textContent = valor;
                console.log('tipo', tipo)
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
                        carregaGrid('T');
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

//Vender Fundo - Início
document.getElementById('btnExcluir').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll("input[type=checkbox]");
     const radios = document.querySelectorAll('input[type="radio"]');

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
        return alert('Nenhum item selecionado para alteração.');
    }

    fetch('/alterar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: idsToDelete, tipo: 3 }),
    })
     .then(response => {
        if (response.status === 200) {
            // Se o status for 204, a exclusão foi bem-sucedida
            checkboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    checkbox.closest('tr').remove(); // Remove as linhas correspondentes
                }
            });
            alert('Itens alterados com sucesso!');
            carregaGrid('T');
            radios.forEach(radio => {
                radio.checked = false;
            });
        } else {
            // Se não for 204, trata como erro
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao alterar itens: ' + error.message);
    });
});
//Vender Fundo - Fim

//Carregar Tela - Início
function carregaGrid(fundo) {
    const tbody = document.getElementById('pAportesBody');
    if (!tbody) {
        console.error('pAportesBody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/pAportes?tipo=${encodeURIComponent(fundo)}`)
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
                responseData.dados.forEach(aportes => { // Correção aqui
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="display: none;">${aportes.ID}</td>
                        <td >${aportes.nm_empressa}</td>
                        <td >${aportes.tipo_fundo}</td>
                        <td >${aportes.ticker}</td>
                        <td >${aportes.vl_investido}</td>
                        <td class="editable" data-col="qtd">${aportes.qtd}</td>
                        <td class="editable" data-col="vl_cota">${aportes.vl_cota}</td>
                        <td>${aportes.vl_total}</td>
                        <td class="editable" data-col="vl_rendimento">${aportes.vl_rendimento}</td>
                        <td><input type="checkbox" value="${aportes.ID}"></td>
                    `;
                    tbody.appendChild(row);
                });
               colunasEditaveis(fundo); //Torna as células editáveis
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="8">Nenhum aporte realizado este mês.</td>'; // Corrigido o colspan
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error.message)); // Mensagem de erro mais descritiva
}
function colunasEditaveis(fundo) {
    const editableCells = document.querySelectorAll('#pAportesBody .editable');

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
        const idTabela = row.querySelectorAll('td')[0].textContent;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const valor = input.value;
                const tipo = 3;
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
                        console.log('aqui2');
                        carregaGrid(fundo);
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