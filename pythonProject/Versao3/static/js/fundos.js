//Incluir Aporte - Início
function extrairValor(campo) {
    const digitos = campo.match(/\d+/); // Captura os dígitos
    return digitos ? digitos[0] : campo; // Retorna os dígitos ou o valor completo
}

document.getElementById('btIncluirFundo').addEventListener('click', function() {
    const campos = {cbTicker: document.getElementById('cbTicker').value};

    const produtosExtraidos = {};
    for (const [key, value] of Object.entries(campos)) {
        produtosExtraidos[key] = extrairValor(value);
    }

   const qtd = document.getElementById('qtd').value;
   const vlCota = document.getElementById('vlAporte').value;
   const vlRend = document.getElementById('vlRendimento').value;
   console.log(produtosExtraidos.cbTicker)
   if (produtosExtraidos.cbTicker === 'cbTicker') {
       return alert('Campo "Ticker" é Obrigatório.');
   }

   if (!qtd) {
       return alert('Campo "Quantidade" é Obrigatório.');
   }

   if (!vlCota) {
       return alert('Campo "Valor" é Obrigatório.');
   }

    fetch('/adicionaAporte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify ({
            idFundo: produtosExtraidos.cbTicker,
            qtd: qtd,
            vlCota: parseFloat(vlCota),
            vlRend: parseFloat(vlRend)
        })
    })
    .then(response => {
        if (response.status === 200) {
            limparCampos();
            carregaGrid('T');
            document.getElementById('mensagem').innerText = 'Aporte adicionado com sucesso!';
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Erro desconhecido');
            });
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('mensagem').innerText = 'Erro ao adicionar fundo: ' + error.message;
    });
});
//Incluir Aporte - Fim

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
    document.getElementById('cbTicker').value = '';
    document.getElementById('qtd').value = '';
    document.getElementById('vlAporte').value = '';
    document.getElementById('vlRendimento').value = '';
}

function carregaGrid(tipo) {
    const tbody = document.getElementById('FundoBody');
    if (!tbody) {
        console.error('tbody não encontrado.');
        return; // Sai da função se tbody não existir
    }

    fetch(`/aportes?tipo=${encodeURIComponent(tipo)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData  => {
            const dados = responseData.dados; // Acesse a lista de dados aqui
            tbody.innerHTML = ''; // Limpa o conteúdo atual

            if (dados && Array.isArray(dados) && dados.length > 0) {
                dados.forEach(fundo => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${fundo.nm_empressa}</td>
                        <td>${fundo.tipo_fundo}</td>
                        <td>${fundo.ticker}</td>
                        <td>${fundo.vl_investido}</td>
                        <td>${fundo.vl_rendimento}</td>
                    `;
                    tbody.appendChild(row);
                });
            }
            else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="5">Nenhuma fundo encontrada.</td>';
                tbody.appendChild(row);
            }
        })
        .catch(error => console.error('Erro ao carregar dados:', error));
}

function carregaTicker(opcao) {
     const comboBox = document.getElementById('cbTicker');
    if (!comboBox) {
        console.error('ComboBox não encontrado.');
        return; // Sai da função se o combobox não existir
    }

    // Limpa as opções atuais, exceto a primeira
    comboBox.innerHTML = '<option value="">Selecione</option>';

    // Faz uma requisição para buscar os tipos disponíveis
   fetch(`/aportes?fundo=${encodeURIComponent(opcao)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro na rede: ' + response.statusText);
            }
            return response.json(); // Espera-se um JSON como resposta
        })
        .then(responseData => {
            const dados = responseData.dados;
            // Supondo que data seja um array de tipos
            if (dados && Array.isArray(dados) && dados.length > 0) {
                dados.forEach(tipo => {
                    const option = document.createElement('option');
                    option.value = tipo; // Assumindo que 'tipo' é o valor que você quer usar
                    option.textContent = tipo; // O texto que será exibido no combobox
                    comboBox.appendChild(option);
                });
            } else {
                console.error('Formato de dados inesperado:', data);
            }
        })
        .catch(error => console.error('Erro ao carregar tipos:', error));
}
//Recarregar tela - Fim