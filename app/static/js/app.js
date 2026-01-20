

console.log("App.js carregado");


/* ===============================
   INICIALIZAÇÃO DOS ÍCONES
================================ */
document.addEventListener("DOMContentLoaded", () => {
    createIcons();
});

/* ===============================
   ELEMENTOS DA UI
================================ */
const listView = document.getElementById('list-view');
const detailView = document.getElementById('detail-view');
const detailContent = document.getElementById('detail-content');
const backToListBtn = document.getElementById('back-to-list');


/* ===============================
   ROUTER VIA HASH
================================ */
function handleRoute() {
    const hash = window.location.hash;

    if (hash.startsWith('#property/')) {
        const id = hash.split('/')[1];

        listView.classList.add('hidden');
        detailView.classList.remove('hidden');

        renderPropertyDetailFromDOM(id);
        window.scrollTo(0, 0);
    } else {
        listView.classList.remove('hidden');
        detailView.classList.add('hidden');
    }
}

/* ===============================
   EVENTOS
================================ */
window.addEventListener('hashchange', handleRoute);

if (backToListBtn) {
    backToListBtn.addEventListener('click', () => {
        window.location.hash = '';
    });
}

const mobileBtn = document.querySelector('.mobile-menu-toggle');
if (mobileBtn) {
    mobileBtn.addEventListener('click', () => {
        alert('Menu mobile em breve 😉');
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const slider = document.getElementById('gallery-slider');
    const dots = document.querySelectorAll('.gallery-dot');

    if (!slider || !dots.length) return;

    // Atualiza o dot ativo ao rolar
    slider.addEventListener('scroll', () => {
        const index = Math.round(slider.scrollLeft / slider.clientWidth);
        dots.forEach((dot, i) => dot.classList.toggle('active', i === index));
    });

    // Clicar no dot move o slider
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const index = parseInt(dot.dataset.index);
            slider.scrollTo({
                left: index * slider.clientWidth,
                behavior: 'smooth'
            });
        });
    });

    // Botão de voltar
    const backBtn = document.querySelector('.btn-back');
    if (backBtn) {
        backBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = '/';
        });
    }
});

/* ===============================
   LOAD INICIAL
================================ */
handleRoute();
