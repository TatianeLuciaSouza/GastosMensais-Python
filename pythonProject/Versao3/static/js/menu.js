async function dadosSQL() {
    const data = await fetch('/menu')
    return await data.json()
}

// Função para gerar as linhas da tabela
function renderTableRows(data) {
    const tableBody = document.getElementById('table-body')
    tableBody.innerHTML = ''

    data.forEach(item => {
      const row = document.createElement('tr')
      row.classList.add('odd:bg-white', 'even:bg-slate-50')

      const nameProdutoCell = document.createElement('td')
      nameCell.textContent = item.nomeProduto

      const nomeLojaCell = document.createElement('td')
      titleCell.textContent = item.nomeLoja

      const valorCell = document.createElement('td')
      emailCell.textContent = item.valor

      const qtdCell = document.createElement('td')
      emailCell.textContent = item.qtd

      const dataCell = document.createElement('td')
      emailCell.textContent = item.data

      row.appendChild(nameProdutoCell)
      row.appendChild(nomeLojaCell)
      row.appendChild(valorCell)
      row.appendChild(qtdCell)
      row.appendChild(dataCell)
      tableBody.appendChild(row)
    })
  }

  // Chame a função para buscar os dados do SQL e renderizar a tabela
  dadosSQL().then(renderTableRows)