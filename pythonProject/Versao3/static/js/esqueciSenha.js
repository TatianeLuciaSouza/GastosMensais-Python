 document.getElementById('EnviaCodigo').addEventListener('click', function() {
            const email = document.getElementById('email').value;

            // Limpar mensagens anteriores
            document.getElementById('mensagem').innerText = '';
            document.getElementById('codigoGerado').innerText = '';

            fetch('/enviaCodigo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('mensagem').innerText = data.message;
                if (data.codigo) {
                    document.getElementById('codigoGerado').innerText = 'Código enviado: ' + data.codigo;
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('mensagem').innerText = 'Erro ao enviar email: ' + error.message;
            });
        });