//Alterar Décimo Tercceiro - Início
document.querySelectorAll('#pDecimoBody .alt').forEach(cell => {
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
                const tipo = 4;
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
//Alterar Décimo Tercceiro - Fim

//Incluir primeira parcela do 13 - Início
document.getElementById('okButton').addEventListener('click', function() {
    const valor = document.getElementById('valor').value;
    console.log('entrouaqui');
    fetch('/adicionar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ valor: valor, tipo: 5 }),
    })
    .then(response => {
        if (response.ok) {
            carregaGrid();
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao incluir primeira parcela do décimo terceiro: ' + error.message);
    });
});
//Incluir primeira parcela do 13 - Fim

//Carregar Tela - Início
function carregaGrid() {
    const tbody = document.getElementById('pDecimoBody');
    if (!tbody) {
        console.error('pDecimoBody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/pDecimo13?tipo=${encodeURIComponent('JS')}`)
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
                responseData.dados.forEach(decimo => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="display: none;">${decimo.ID}</td>
                        <td class="editable" data-col="vlParcela1">${decimo.vlParcela1}</td>
                        <td class="editable" data-col="vlParcela2">${decimo.vlParcela2}</td>
                        <td >${decimo.vlTotal}</td>
                        <td >${decimo.vlSobra}</td>
                    `;
                    tbody.appendChild(row);
                });
                 colunasEditaveis(); //Torna as células editáveis
                 //document.getElementById('valorLabel').style.display = 'none';
                 //document.getElementById('valor').style.display = 'none';
                 //document.getElementById('okButton').style.display = 'none';
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="8">Não há Décimo Terceiro ainda este ano.</td>'; // Corrigido o colspan
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error.message)); // Mensagem de erro mais descritiva
}

function colunasEditaveis() {
    const editableCells = document.querySelectorAll('#pDecimoBody .editable');

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
                const tipo = 4;
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