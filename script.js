console.log("%cWelcome fellow developer. Green means good, so all is good right?", "color: #1eff00; font-size: 16px; font-weight: bold; font-family: Cascadia Code;")

const starCount = 300;

for (let i = 0; i < starCount; i++) {
    const star = document.createElement('div');
    star.className = 'star';

    const size = Math.random() * 3 + 1; // Size between 1-4px
    star.style.width = size + 'px';
    star.style.height = size + 'px';
    star.style.left = Math.random() * 100 + '%';
    star.style.top = Math.random() * 100 + '%';
    star.style.opacity = 0; // Start fully invisible
    star.style.animationDelay = Math.random() * 5 + 's';

    document.body.appendChild(star);
}