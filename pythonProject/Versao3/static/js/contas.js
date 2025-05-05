//Incluir Conta - Início
function extrairValor(campo) {
    const digitos = campo.match(/\d+/); // Captura os dígitos
    return digitos ? digitos[0] : campo; // Retorna os dígitos ou o valor completo
}

document.getElementById('btIncluirConta').addEventListener('click', function() {
       const campos = {
            cbContas: document.getElementById('cbContas').value,
            cbTpContas: document.getElementById('cbTpContas').value
        };

    const produtosExtraidos = {};
    for (const [key, value] of Object.entries(campos)) {
        produtosExtraidos[key] = extrairValor(value);
    }

    const desc = document.getElementById('desc').value;
    const valorConta = document.getElementById('valorConta').value;
    const parcelas = document.getElementById('parcelas').value;
    const tipo = 2;

    if (!produtosExtraidos.cbContas) {
        return alert('Campo "Conta" é Obrigatório.');
    }

    if (!produtosExtraidos.cbTpContas === 'opcao') {
        return alert('Campo "Tipo de Conta" é Obrigatório.');
    }

    if (!valorConta) {
        return alert('Campo "Valor da Conta" é Obrigatório.');
    }

    if (!parcelas) {
        return alert('Campo "Parcelas" é Obrigatório.');
    }

    fetch('/adicionar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify ({
            cbContas: produtosExtraidos.cbContas,
            cbTpContas: produtosExtraidos.cbTpContas,
            desc: desc,
            parcelas: parcelas,
            valorConta: parseFloat(valorConta),
            tipo: tipo
        })
    })
    .then(response => {
        if (response.status === 200) {
            limparCampos();
            document.getElementById('mensagem').innerText = 'Conta adicionado com sucesso!';
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('mensagem').innerText = 'Erro ao adicionar conta: ' + error.message;
    });
});

//Incluir Conta - Fim

//Recarregar tela - Início
function limparCampos() {
    document.getElementById('cbContas').value = '';
    document.getElementById('cbTpContas').value = '';
    document.getElementById('desc').value = '';
    document.getElementById('parcelas').value = '';
    document.getElementById('valorConta').value = '';
}
//Recarregar tela - Fim