document.addEventListener('DOMContentLoaded', function () {
    // Цвета для оценок от 0.5 до 5.0
    const ratingColors = [
        '#FF0000', '#FF2000', '#FF4000', '#FF4F00', '#FF6F00',
        '#FF9900', '#FFBF00', '#CAED07', '#5FCA15', '#29B81C'
    ];
    const emptyColor = '#CCCCCC';

    function hexToRgba(hex, alpha) {
        const r = parseInt(hex.slice(1,3), 16);
        const g = parseInt(hex.slice(3,5), 16);
        const b = parseInt(hex.slice(5,7), 16);
        return `rgba(${r},${g},${b},${alpha})`;
    }

    function colorForValue(val) {
        if (val <= 0) return emptyColor;
        const index = Math.round((val - 0.5) * 2);
        return ratingColors[index] || emptyColor;
    }

    // Рендеринг звёзд для среднего рейтинга (некликабельный)
    function renderAverageStars(container, rating) {
        const rounded = Math.round(rating * 2) / 2;   // округление до 0.5
        const fillColor = colorForValue(rounded);
        container.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.textContent = '★';
            let fillLevel = 0;
            if (i <= Math.floor(rounded)) {
                fillLevel = 1;
            } else if (i === Math.floor(rounded) + 1 && (rounded - Math.floor(rounded)) >= 0.5) {
                fillLevel = 0.5;
            }

            if (fillLevel === 1) {
                star.style.color = fillColor;
                star.style.opacity = 1;
            } else if (fillLevel === 0.5) {
                const left = fillColor;
                const right = hexToRgba(fillColor, 0.25);
                star.style.background = `linear-gradient(to right, ${left} 0%, ${left} 50%, ${right} 50%, ${right} 100%)`;
                star.style.webkitBackgroundClip = 'text';
                star.style.backgroundClip = 'text';
                star.style.color = 'transparent';
            } else {
                star.style.color = fillColor;
                star.style.opacity = 0.25;
            }
            star.style.fontSize = '1.5rem';
            container.appendChild(star);
        }
    }

    // --- Интерактивные звёзды для формы (уже были) ---
    const container = document.getElementById('rating-stars-container');
    if (container) {
        // ... (оставь текущий код для формы без изменений)
    }

    // ---------- Средний рейтинг ----------
const avgContainer = document.getElementById('avg-rating-stars');
if (avgContainer) {
    const rating = parseFloat(avgContainer.dataset.rating) || 0;
    renderAverageStars(avgContainer, rating);
}

// ---------- Звёзды для каждого отзыва ----------
document.querySelectorAll('.review-rating-stars').forEach(span => {
    const rating = parseFloat(span.dataset.rating) || 0;
    renderAverageStars(span, rating);
});
});