//Incluir Compra - Início
function extrairValor(campo) {
    const digitos = campo.match(/\d+/); // Captura os dígitos
    return digitos ? digitos[0] : campo; // Retorna os dígitos ou o valor completo
}

async function conferirSalario() {
    try {
        const response = await fetch(`/verificacao?tipo=${encodeURIComponent(1)}`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`Erro na rede: ${response.statusText} - ${errorData.message || 'Sem detalhes'}`);
        }
        const responseData = await response.json();
        return responseData && Array.isArray(responseData.salario) && responseData.salario.length > 0 ? 1 : 0;
    } catch (error) {
        console.error('Erro ao conferir salário:', error);
        alert('Erro ao conferir salário: ' + error.message);
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
        console.error('Erro ao conferir o saldo do salário:', error);
        alert('Erro ao conferir o saldo do salário: ' + error.message);
        return 0;
    }
}

document.getElementById('btnAdicionar').addEventListener('click', async function() {
    const campos = {
        cbProduto: document.getElementById('cbProduto').value,
        cbTpProduto: document.getElementById('cbTpProduto').value,
        cbloja: document.getElementById('cbloja').value,
    };

    const produtosExtraidos = {};
    for (const [key, value] of Object.entries(campos)) {
        produtosExtraidos[key] = extrairValor(value);
    }

    const cbTpLocal = document.getElementById('cbTpLocal').value;
    const valor = document.getElementById('valor').value;
    const quantidade = document.getElementById('qtd').value;

    if (!produtosExtraidos.cbProduto) {
        return alert('Campo "Nome Produto" é Obrigatório.');
    }

    if (produtosExtraidos.cbTpProduto === 'opcao') {
        return alert('Campo "Tipo do Produto" é Obrigatório.');
    }

    if (!produtosExtraidos.cbloja) {
        return alert('Campo "Loja" é Obrigatório.');
    }
        console.log('cbTpLocal', cbTpLocal)

    if (cbTpLocal === 'opcao') {
        return alert('Campo "Tipo da Loja" é Obrigatório.');
    }

    if (!valor) {
         return alert('Campo "Valor" é Obrigatório.');
    }

    if (!quantidade) {
        return alert('Campo "Quantidade Compra" é Obrigatório.');
    }

    const salario = await conferirSalario();
    if (salario === 0) {
        limparCampos();
        return alert('Você não possui salário este mês.');
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
            cbProduto: produtosExtraidos.cbProduto,
            cbTpProduto: produtosExtraidos.cbTpProduto,
            cbloja: produtosExtraidos.cbloja,
            cbTpLocal: cbTpLocal,
            valor: parseFloat(valor),
            quantidade: parseInt(quantidade),
            tipo: 1
        })
    })
    .then(response => {
        if (response.status === 200) {
            limparCampos();
            carregaGrid();
            document.getElementById('mensagem').innerText = 'Gasto adicionado com sucesso!';
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('mensagem').innerText = 'Erro ao adicionar compra: ' + error.message;
    });
});

//Incluir Compra - Fim

//Excluir Compra - Início
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

    if (idsToDelete.length === 0) {
        return alert('Nenhum item selecionado para exclusão.');
    }

    fetch('/deletar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idTabela: idsToDelete, tipo: 1 }),
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
//Excluir Compra - Fim

//Recarregar tela - Início
function limparCampos() {
    document.getElementById('cbProduto').value = '';
    document.getElementById('cbTpProduto').value = '';
    document.getElementById('cbloja').value = '';
    document.getElementById('cbTpLocal').value = '';
    document.getElementById('valor').value = '';
    document.getElementById('qtd').value = '';
}

function carregaGrid() {
    const tbody = document.getElementById("gastosBody");
    if (!tbody) {
        console.error('gastosBody não encontrado.');
        return;
    }

    fetch(`/gastos?tipo=${encodeURIComponent('JS')}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData  => {
            tbody.innerHTML = ''; // Limpa o conteúdo atual
            if (responseData && Array.isArray(responseData.dados) && responseData.dados.length > 0) {
                responseData.dados.forEach(gastos => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${gastos.Produto}</td>
                        <td>${gastos.Loja}</td>
                        <td>${gastos.Valor}</td>
                        <td>${gastos.Qtd}</td>
                        <td>${gastos.vlTotal}</td>
                        <td><input type="checkbox" value="${gastos.ID}"></td>
                        <td style="display: none;">${gastos.ID}</td>
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