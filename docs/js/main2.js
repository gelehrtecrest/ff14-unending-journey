
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const searchBox = document.getElementById('search-box');

    // Theme switching
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.body.classList.add(currentTheme + '-mode');
    themeToggle.textContent = currentTheme === 'light' ? '
D83C
DF19' : '
2600
FE0F';

    themeToggle.addEventListener('click', () => {
        let newTheme = document.body.classList.contains('light-mode') ? 'dark' : 'light';
        document.body.classList.remove('light-mode', 'dark-mode');
        document.body.classList.add(newTheme + '-mode');
        localStorage.setItem('theme', newTheme);
        themeToggle.textContent = newTheme === 'light' ? '
D83C
DF19' : '
2600
FE0F';
    });

    // Search functionality
    searchBox.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.card');

        cards.forEach(card => {
            const title = card.querySelector('h3').textContent.toLowerCase();
            const links = card.querySelectorAll('ul li a');
            let hasMatch = false;

            if (title.includes(searchTerm)) {
                hasMatch = true;
            }

            links.forEach(link => {
                if (link.textContent.toLowerCase().includes(searchTerm)) {
                    hasMatch = true;
                }
            });

            if (hasMatch) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
