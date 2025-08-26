document.addEventListener('DOMContentLoaded', () => {

    // --- Theme Toggler --- //
    const themeToggleButton = document.getElementById('theme-toggle-button');
    const htmlElement = document.documentElement;

    // Function to set theme
    const setTheme = (theme) => {
        htmlElement.setAttribute('data-bs-theme', theme);
        localStorage.setItem('theme', theme);
        // Update icon
        const icon = themeToggleButton.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('bi-moon-stars-fill');
            icon.classList.add('bi-sun-fill');
        } else {
            icon.classList.remove('bi-sun-fill');
            icon.classList.add('bi-moon-stars-fill');
        }
    };

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    setTheme(savedTheme);

    // Toggle theme on button click
    themeToggleButton.addEventListener('click', () => {
        const currentTheme = htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });

    // --- Search Functionality --- //
    const searchBox = document.getElementById('search-box');
    const cards = document.querySelectorAll('.card-item');

    searchBox.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();

        cards.forEach(card => {
            const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
            const cardLinks = Array.from(card.querySelectorAll('a')).map(a => a.textContent.toLowerCase());
            const cardText = cardTitle + ' ' + cardLinks.join(' ');

            const parentCol = card.closest('.col');

            if (cardText.includes(searchTerm)) {
                parentCol.classList.remove('hide');
            } else {
                parentCol.classList.add('hide');
            }
        });
    });
});
