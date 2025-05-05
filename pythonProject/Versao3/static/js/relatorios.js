document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('cbRelatorio').addEventListener('change', function() {
        const selectedOption = this.value;
        // Habilita ou desabilita campos com base na opção selecionada
        const produtosSelect = document.getElementById('cbProduto');
        const tipoProdutoSelect = document.getElementById('cbTpProduto');
        const local13Select = document.getElementById('cbLocal13');
        const tipoLocal13Select = document.getElementById('cbTpLocal13');
        const dataInicioInput = document.getElementById('dataInicio');
        const dataFimInput = document.getElementById('dataFim');
        const gerarButton = document.getElementById('btnGerar');
        const checkboxes = document.querySelectorAll('input[name="opcao"]');

        // Reseta os campos
        produtosSelect.disabled = false;
        tipoProdutoSelect.disabled = false;
        local13Select.disabled = false;
        tipoLocal13Select.disabled = false;
        dataInicioInput.disabled = false;
        dataFimInput.disabled = false;
        gerarButton.disabled = false;
        checkboxes.forEach(checkbox => {
            checkbox.disabled = false;
        });

        // Carrega produtos e habilita campos com base na opção selecionada
        switch (selectedOption) {
            case 'rGastos':
            case 'rGastos13':
                document.getElementById('produto').innerText = 'Nome da Produto:';
                document.getElementById('tpProduto').innerText = 'Tipo do Produto:';

                fetch(`/consultaRelatorio?tipo_relatorio=${selectedOption}`)
                .then(response => response.json())
                .then(data => {
                     produtosSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                     tipoProdutoSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                     local13Select.innerHTML = '<option value="">Selecione uma Opção</option>';

                     const produtos = data.produtos;
                     const tpProdutos = data.tpProdutos;
                     const loja = data.loja;

                     if (produtos && Array.isArray(produtos) && produtos.length > 0) {
                        produtos.forEach(prod => {
                            const option = document.createElement('option');
                            option.value = prod;
                            option.textContent = prod;
                            produtosSelect.appendChild(option);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }

                     if (tpProdutos && Array.isArray(tpProdutos) && tpProdutos.length > 0) {
                        tpProdutos.forEach(tpProd => {
                            const option2 = document.createElement('option');
                            option2.value = tpProd;
                            option2.textContent = tpProd;
                            tipoProdutoSelect.appendChild(option2);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }

                     if (loja && Array.isArray(loja) && loja.length > 0) {
                        loja.forEach(loja => {
                            const option3 = document.createElement('option');
                            option3.value = loja;
                            option3.textContent = loja;
                            local13Select.appendChild(option3);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }

                    checkboxes.forEach(checkbox => {
                        checkbox.disabled = true;
                    });
                });
                break;

            case 'rContas':
                document.getElementById('produto').innerText = 'Nome da Conta:';
                document.getElementById('tpProduto').innerText = 'Tipo da Conta:';

                fetch(`/consultaRelatorio?tipo_relatorio=${selectedOption}`)
                .then(response => response.json())
                .then(data => {
                     produtosSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                     tipoProdutoSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                     local13Select.innerHTML = '<option value="">Selecione uma Opção</option>';

                     const produtos = data.produtos;
                     const tpProdutos = data.tpProdutos;
                     const loja = data.loja;

                     if (produtos && Array.isArray(produtos) && produtos.length > 0) {
                        produtos.forEach(prod => {
                            const option = document.createElement('option');
                            option.value = prod;
                            option.textContent = prod;
                            produtosSelect.appendChild(option);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }

                     if (tpProdutos && Array.isArray(tpProdutos) && tpProdutos.length > 0) {
                        tpProdutos.forEach(tpProd => {
                            const option2 = document.createElement('option');
                            option2.value = tpProd;
                            option2.textContent = tpProd;
                            tipoProdutoSelect.appendChild(option2);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }

                     if (loja && Array.isArray(loja) && loja.length > 0) {
                        loja.forEach(loja => {
                            const option3 = document.createElement('option');
                            option3.value = loja;
                            option3.textContent = loja;
                            local13Select.appendChild(option3);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }
                });
                break;

            case 'rMetas':
                document.getElementById('produto').innerText = 'Nome da Meta:';

                fetch(`/consultaRelatorio?tipo_relatorio=${selectedOption}`)
                .then(response => response.json())
                .then(data => {
                     produtosSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                     const metas = data.metas;
                     if (metas && Array.isArray(metas) && metas.length > 0) {
                        metas.forEach(meta => {
                            const option = document.createElement('option');
                            option.value = meta;
                            option.textContent = meta;
                            produtosSelect.appendChild(option);
                        });
                     } else {
                        console.error('Formato de dados inesperado:', data);
                     }
                });

                tipoProdutoSelect.disabled = true;
                local13Select.disabled = true;
                tipoLocal13Select.disabled = true;
                break;

             case 'rAportes':
                document.getElementById('produto').innerText = 'Tipo do Investimento:';
                document.getElementById('tpProduto').innerText = 'Ticker:';

                produtosSelect.innerHTML = '<option value="">Selecione uma Opção</option>';
                const produtosAportes = ['Fundos de Investimento', 'Ações'];
                produtosAportes.forEach(produto => {
                    const option = document.createElement('option');
                    option.value = produto;
                    option.textContent = produto;
                    produtosSelect.appendChild(option);
                });

                produtosSelect.addEventListener('change', function() {
                    const selectedProduto = this.value;
                    const fundo = selectedProduto === 'Fundos de Investimento' ? 'F' : 'A';

                    fetch(`/consultaRelatorio?tipo_relatorio=${selectedOption}&fundo=${fundo}`)
                        .then(response => response.json())
                        .then(data => {
                            tipoProdutoSelect.innerHTML = '<option value="">Selecione um Tipo</option>';
                            const tickers = data.tickers; // Renomeado para manter a clareza

                            if (tickers && Array.isArray(tickers)) {
                                tickers.forEach(ticker => {
                                    const option = document.createElement('option');
                                    option.value = ticker;
                                    option.textContent = ticker;
                                    tipoProdutoSelect.appendChild(option);
                                });
                            } else {
                                console.error('Formato de dados inesperado:', data);
                            }
                        });
                });

                local13Select.disabled = true;
                tipoLocal13Select.disabled = true;
                gerarButton.disabled = true;
                dataInicioInput.disabled = true;
                dataFimInput.disabled = true;
                break;

            case 'rDecimo13':
                produtosSelect.disabled = true;
                tipoProdutoSelect.disabled = true;
                local13Select.disabled = true;
                tipoLocal13Select.disabled = true;
                dataInicioInput.disabled = true;
                dataFimInput.disabled = true;
                gerarButton.disabled = true;
                checkboxes.forEach(checkbox => {
                    checkbox.disabled = true;
                });
                break;

            default:
                produtosSelect.disabled = true;
                tipoProdutoSelect.disabled = true;
                local13Select.disabled = true;
                tipoLocal13Select.disabled = true;
                dataInicioInput.disabled = true;
                dataFimInput.disabled = true;
                gerarButton.disabled = true;
                checkboxes.forEach(checkbox => {
                    checkbox.disabled = true;
                });
                break;

        }
    });
});