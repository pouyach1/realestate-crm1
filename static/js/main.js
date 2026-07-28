/**
 * Estate Basic - Main JavaScript
 * نسخه بهینه و حرفه‌ای
 */

// ========================================
// UTILS
// ========================================
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

function getCSRF() {
    return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
}

// ========================================
// NAVBAR SCROLL
// ========================================
const navbar = $('#mainNav');
if (navbar) {
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
}

// ========================================
// SMOOTH SCROLL
// ========================================
$$('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
        const target = $(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// ========================================
// FAVORITES - علاقه‌مندی
// ========================================
$$('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', async function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const icon = $('i', this);
        const heart = icon.classList.contains('bi-heart-fill');
        
        // آپدیت فوری UI (optimistic)
        icon.classList.toggle('bi-heart');
        icon.classList.toggle('bi-heart-fill');
        this.style.color = heart ? '#ccc' : '#e74c3c';
        
        try {
            const res = await fetch('/properties/toggle-favorite/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRF(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `property_id=${this.dataset.propertyId}`
            });
            
            if (!res.ok) throw new Error('Network error');
            
        } catch (err) {
            // برگردون به حالت قبل
            icon.classList.toggle('bi-heart');
            icon.classList.toggle('bi-heart-fill');
            this.style.color = heart ? '#e74c3c' : '#ccc';
        }
    });
});

// ========================================
// SLIDER - فروش ویژه
// ========================================
const slider = $('#urgentRow');
if (slider) {
    const scroll = () => {
        const max = slider.scrollWidth - slider.clientWidth;
        if (slider.scrollLeft <= 5) slider.scrollTo({ left: max, behavior: 'smooth' });
        else slider.scrollBy({ left: -340, behavior: 'smooth' });
    };
    setInterval(scroll, 4000);
}