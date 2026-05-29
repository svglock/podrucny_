// Восстанавливает значения фильтров из data-атрибутов формы
function restoreFilters(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    // Чекбоксы
    const checkboxes = form.querySelectorAll('input[type="checkbox"][data-checked]');
    checkboxes.forEach(cb => {
        cb.checked = cb.dataset.checked === 'true';
    });

    // Селекты
    const selects = form.querySelectorAll('select[data-selected]');
    selects.forEach(sel => {
        sel.value = sel.dataset.selected;
    });
}

// Универсальная установка значения в поле
function setValue(fieldId, value) {
    const field = document.getElementById(fieldId);
    if (field) field.value = value;
}

// Применяем восстановление после загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    // Если на странице есть форма с id "supplier-filter-form"
    restoreFilters('supplier-filter-form');
    restoreFilters('courier-filter-form');
    restoreFilters('product-filter-form');
});