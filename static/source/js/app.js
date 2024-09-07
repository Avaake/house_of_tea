function updateMinValue(value) {
    document.getElementById('minValue').textContent = value;
}

function updateMaxValue(value) {
    document.getElementById('maxValue').textContent = value;
}

document.addEventListener('DOMContentLoaded', function () {
    const deliveryAddressField = document.getElementById('deliveryAddressField');
    const deliveryOptions = document.querySelectorAll('input[name="requires_delivery"]');

    function toggleDeliveryField() {
        if (document.getElementById('delivery_np').checked) {
            deliveryAddressField.style.display = 'block';
        } else {
            deliveryAddressField.style.display = 'none';
        }
    }

    // При зміні опції викликати toggleDeliveryField
    deliveryOptions.forEach(option => {
        option.addEventListener('change', toggleDeliveryField);
    });

    // Встановити початковий стан поля
    toggleDeliveryField();
});