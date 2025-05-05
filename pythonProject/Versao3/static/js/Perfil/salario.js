//Alterar Salário - Início
document.querySelectorAll('#pSalarioBody .alt').forEach(cell => {
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
                const tipo = 5;
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
//Alterar Salário - Fim

//Incluir Salário - Início
document.getElementById('okButton').addEventListener('click', function() {
    const salario = document.getElementById('vlSalario').value;
    const extra = document.getElementById('vlExtra').value;

    fetch('/adicionar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ valor1: salario, valor2: extra, tipo: 6 }),
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
        alert('Erro ao incluir salário do mês: ' + error.message);
    });
});
//Incluir Salário - Fim

//Carregar Tela - Início
function carregaGrid() {
    const tbody = document.getElementById('pSalarioBody');
    if (!tbody) {
        console.error('pSalarioBody não encontrado.');
        return;
    }

    fetch(`/perfilSalario?tipo=${encodeURIComponent('JS')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json();
        })
        .then(responseData => {
            tbody.innerHTML = '';

            if (responseData && Array.isArray(responseData.dados) && responseData.dados.length > 0) {
                responseData.dados.forEach(sal => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td style="display: none;">${sal.ID}</td>
                        <td class="editable" data-col="salario">${sal.salario}</td>
                        <td>${sal.sobra}</td>
                        <td>${sal.gastos}</td>
                        <td class="editable" data-col="extra">${sal.extra}</td>
                    `;
                    tbody.appendChild(row);
                });
                colunasEditaveis();
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="8">Não há salário este mês.</td>';
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error.message));
}

function colunasEditaveis() {
    const editableCells = document.querySelectorAll('#pSalarioBody .editable');

    editableCells.forEach(cell => {
        cell.addEventListener('click', function() {
        const originalText = cell.textContent;
        const input = document.createElement('input');
        input.value = originalText;
        cell.innerHTML = '';
        cell.appendChild(input);
        const coluna = cell.cellIndex;
        input.focus();
        const row = cell.closest('tr');
        const idTabela = row.querySelectorAll('td')[0].textContent;

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const valor = input.value;
                const tipo = 5;
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
                    })
                })

                .then(response => {
                    if (response.status === 200) {
                        console.log('aqui2');
                        carregaGrid();
                    } else {
                        console.error('Erro ao atualizar:', data.error);
                        cell.textContent = originalText;
                    }
                });
            }
        });

        input.addEventListener('blur', () => {
            cell.textContent = originalText;
        });
    });
    });
}
//Carregar Tela - Fim