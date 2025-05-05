function hideLabel(input) {
        input.previousElementSibling.style.display = 'none';
      }

function showLabel(input) {
    if (input.value.trim() === '') {
          input.previousElementSibling.style.display = 'inline';
    }
}

const tabs = document.querySelectorAll('.tab');
const tabContent = document.querySelectorAll('.tab-content > div');

tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
        console.log('Clicou no tab', index);
        // Oculta todos os conteúdos
        tabContent.forEach(content => content.style.display = 'none');

        // Exibe o conteúdo correspondente
        tabContent[index].style.display = 'block';
    });
});