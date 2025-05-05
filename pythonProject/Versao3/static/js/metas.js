//Incluir Meta - Início
document.getElementById('btIncluirMeta').addEventListener('click', function() {
   const checkboxes = document.querySelectorAll('input[name="opcao"]');
   let value;
   checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            value = checkbox.value;
        }
    });

   const meta = document.getElementById('meta').value;
   const vlInicial = document.getElementById('vlInicialMeta').value;
   const vlFinal = document.getElementById('vlFinalMeta').value;
   const vlMensal = document.getElementById('vlMensalMeta').value;
   const tipo = 3;

   if (!value) {
       return alert('Informar como será descontado é Obrigatório.');
   }

   if (!meta) {
       return alert('Campo "Meta" é Obrigatório.');
   }

   if (!vlMensal) {
       return alert('Campo "Valor Mensal" é Obrigatório.');
   }

    fetch('/adicionar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify ({
            mov: value,
            meta: meta,
            vlInicial: parseFloat(vlInicial),
            vlFinal: parseFloat(vlFinal),
            vlMensal: parseFloat(vlMensal),
            tipo: tipo
        })
    })
    .then(response => {
        if (response.status === 200) {
            limparCampos();
            atualizarTabela('A');
            document.getElementById('mensagem').innerText = 'Meta adicionado com sucesso!';
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('mensagem').innerText = 'Erro ao adicionar meta: ' + error.message;
    });
});
//Incluir Meta - Fim

const checkboxes = document.querySelectorAll('input[name="status"]');

// Adiciona um evento de click a cada checkbox
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function(event) {
        const value = event.target.value; // Captura o valor do checkbox clicado
        atualizarTabela(value);
    });
});

// Função para atualizar a visibilidade da coluna "Data Fim"
function atualizarTabela(status) {
    const dataFimColuna = document.querySelector('.data-fim');

    if (status === 'A') {
        // Oculta o cabeçalho da coluna "Data Fim"
        dataFimColuna.style.display = 'none';

        // Oculta as células da coluna em cada linha do tbody
        const rows = document.querySelectorAll('tr');

        console.log('depois3')
        fetch(`/metas?tipo=${encodeURIComponent(status)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        console.log('antes2')
        carregaGrid(status)
        console.log('depois')
    } else {
        console.log('entrou aqui')
        // Mostra o cabeçalho da coluna "Data Fim"
        dataFimColuna.style.display = '';

        // Mostra as células da coluna em cada linha do tbody
        const rows = document.querySelectorAll('tr');
        carregaGrid(status)
    }
}

//Encerrar Meta - Início
document.getElementById('btnFinalizar').addEventListener('click', function() {
    const checkboxes = document.querySelectorAll("input[type=checkbox]");

    // Array para armazenar os IDs dos checkboxes selecionados
    const idsToDelete = [];

    // Itera sobre todos os checkboxes
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) { // Verifica se o checkbox está marcado
            idsToDelete.push(checkbox.value); // Adiciona o valor ao array
        }
    });

    console.log('Selecionados', checkboxes);
    console.log('IDs a serem excluídos:', idsToDelete); // Para depuração

    if (idsToDelete.length === 0) {
        return alert('Nenhum item selecionado para exclusão.');
    }

    fetch('/deletar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idTabela: idsToDelete, tipo: 2 }),
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
//Encerrar Meta - Fim

//Recarregar tela - Início
function limparCampos() {
    document.getElementById('meta').value = '';
    document.getElementById('vlInicialMeta').value = '';
    document.getElementById('vlFinalMeta').value = '';
    document.getElementById('vlMensalMeta').value = '';
}

function carregaGrid(tipo) {
    const tbody = document.getElementById('metasBody');
    if (!tbody) {
        console.error('tbody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/metas?tipo=${encodeURIComponent(tipo)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData  => {
            const dados = responseData.dados; // Acesse a lista de dados aqui
            tbody.innerHTML = ''; // Limpa o conteúdo atual

            if (tipo == 'A') {
                 if (dados && Array.isArray(dados) && dados.length > 0) {
                    dados.forEach(meta => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${meta.meta}</td>
                        <td>${meta.dtInicio}</td>
                        <td>${meta.vlAtual}</td>
                        <td>${meta.vlFinal}</td>
                        <td><input type="checkbox" value="${meta.ID}"></td>
                        <td style="display: none;">${meta.ID}</td>
                    `;
                    tbody.appendChild(row);
                });
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="5">Nenhuma meta encontrada.</td>';
                    tbody.appendChild(row);
                }
            }
            else {
                if (dados && Array.isArray(dados) && dados.length > 0) {
                dados.forEach(meta => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${meta.meta}</td>
                        <td>${meta.dtInicio}</td>
                        <td>${meta.dtFinal}</td>
                        <td>${meta.vlAtual}</td>
                        <td>${meta.vlFinal}</td>
                        <td><input type="checkbox" value="${meta.ID}"></td>
                        <td style="display: none;">${meta.ID}</td>
                    `;
                    tbody.appendChild(row);
                });
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="5">Nenhuma meta encontrada.</td>';
                    tbody.appendChild(row);
                }
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
}
//Recarregar tela - Fim
