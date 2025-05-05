async function conferirDecimo() {
    try {
        const response = await fetch(`/verificacao?tipo=${encodeURIComponent(3)}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro na rede: ${response.statusText} - ${errorData.message || 'Sem detalhes'}`);
        }
        const responseData = await response.json();
        return responseData && Array.isArray(responseData.decimo) && responseData.decimo.length > 0 ? 1 : 0;
    } catch (error) {
        console.error('Erro ao conferir décimo:', error);
        alert('Erro ao conferir décimo: ' + error.message);
        return 0;
    }
}

async function conferirSaldo() {
    try {
        const response = await fetch(`/verificacao?tipo=${encodeURIComponent(4)}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro na rede: ${response.statusText} - ${errorData.message || 'Sem detalhes'}`);
        }
        const responseData = await response.json();
        return responseData && Array.isArray(responseData.saldo) && responseData.saldo.length > 0 ? responseData.saldo : 0;
    } catch (error) {
        console.error('Erro ao conferir o saldo do décimo:', error);
        alert('Erro ao conferir o saldo do décimo: ' + error.message);
        return 0;
    }
}

//Incluir Aporte - Início
function extrairValor(campo) {
    const digitos = campo.match(/\d+/); // Captura os dígitos
    return digitos ? digitos[0] : campo; // Retorna os dígitos ou o valor completo
}

document.getElementById('btIncluir').addEventListener('click', async function() {
    const campos = {
        cbProduto: document.getElementById('cbProduto13').value,
        cbTpProduto: document.getElementById('cbTpProduto13').value,
        cbloja: document.getElementById('cbLocal13').value,
    };

    const produtosExtraidos = {};
    for (const [key, value] of Object.entries(campos)) {
        produtosExtraidos[key] = extrairValor(value);
    }

    const tpLoja = document.getElementById('cbTpLocal13').value;
    const qtd = document.getElementById('qtd').value;
    const valor = document.getElementById('valor13').value;
    const desc = document.getElementById('desc').value;
    const tipo = 4;

    if (!produtosExtraidos.cbProduto) {
        return alert('Campo "Nome Produto" é Obrigatório.');
    }

    if (produtosExtraidos.cbTpProduto === 'opcao') {
        return alert('Campo "Tipo do Produto" é Obrigatório.');
    }

    if (!produtosExtraidos.cbloja) {
        return alert('Campo "Onde Comprou" é Obrigatório.');
    }
        console.log('cbTpLocal', cbTpLocal)

    if (cbTpLocal === 'opcao') {
        return alert('Campo "Tipo da Localização" é Obrigatório.');
    }

    if (!valor) {
        return alert('Campo "Valor da Compra" é Obrigatório.');
    }

    if (!qtd) {
        return alert('Campo "Quantidade Compra" é Obrigatório.');
    }

    const decimo = await conferirDecimo();
    if (decimo === 0) {
        limparCampos();
        return alert('Você não possui décimo terceiro este ano.');
    }

     const saldo = await conferirSaldo();
     if (saldo < parseFloat(valor)) {
        limparCampos();
        return alert('Seu saldo é,' + saldo + ',insuficiente para a compra.');
    }

    fetch('/adicionar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify ({
            produto: produtosExtraidos.cbProduto,
            tpProduto: produtosExtraidos.cbTpProduto,
            loja: produtosExtraidos.cbloja,
            tpLoja: tpLoja,
            qtd: parseInt(qtd),
            valor: parseFloat(valor),
            desc: desc,
            tipo: tipo
        })
    })
    .then(response => {
        if (response.status === 200) {
            limparCampos();
            carregaGrid();
            document.getElementById('mensagem').innerText = 'Aporte adicionado com sucesso!';
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('mensagem').innerText = 'Erro ao adicionar gasto do Décimo Terceiro: ' + error.message;
    });
});
//Incluir Aporte - Fim

//Deletar gasto 13 - Início
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
        body: JSON.stringify({ idTabela: idsToDelete, tipo: 3 }),
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
            carregaGrid();
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
//Deletar gasto 13 - Fim


//Alterar Consulta - Início
const checkboxes = document.querySelectorAll('input[name="fundo"]');
const opcao = document.querySelectorAll('input[name="opcao"]');

// Adiciona um evento de click a cada checkbox
checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', function(event) {
        const value = event.target.value; // Captura o valor do checkbox clicado
        carregaGrid(value);
    });
});

opcao.forEach(checkbox => {
    checkbox.addEventListener('click', function(event) {
        const value = event.target.value; // Captura o valor do checkbox clicado
        carregaTicker(value);
    });
});
//Alterar Consulta - Fim

//Recarregar tela - Início
function limparCampos() {
    document.getElementById('cbProduto13').value = '';
    document.getElementById('cbTpProduto13').value = '';
    document.getElementById('cbLocal13').value = '';
    document.getElementById('cbTpLocal13').value = '';
    document.getElementById('qtd').value = '';
    document.getElementById('valor13').value = '';
    document.getElementById('desc').value = '';
}

function carregaGrid() {
    const tbody = document.getElementById('decimoBody');
    if (!tbody) {
        console.error('tbody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/decimo?tipo=${encodeURIComponent('JS')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData  => {
            const dados = responseData.dados; // Acesse a lista de dados aqui
            const titulo = responseData.valor13;
            const nome = responseData.user_name;
            const mensagem = `${nome}, seu saldo do Décimo Terceiro é, ${titulo}`;
            tbody.innerHTML = ''; // Limpa o conteúdo atual
            document.getElementById('titulo').textContent = mensagem;
            if (dados && Array.isArray(dados) && dados.length > 0) {
                dados.forEach(decimo => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${decimo.produto}</td>
                        <td>${decimo.descricao}</td>
                        <td>${decimo.loja}</td>
                        <td>${decimo.valor}</td>
                        <td>${decimo.dt_inclusao}</td>
                        <td><input type="checkbox" value="${decimo.ID}"></td>
                        <td style="display: none;">${decimo.ID}</td>
                    `;
                    tbody.appendChild(row);
                });
            }
            else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="5">Nenhuma gasto do décimo terceiro encontrada.</td>';
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
}
//Recarregar tela - Fim