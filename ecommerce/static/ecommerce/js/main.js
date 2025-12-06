// Main JavaScript for Ecommerce Store

document.addEventListener('DOMContentLoaded', function() {
    // Form Validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Quantity Input Validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const max = parseInt(this.getAttribute('max'));
            const min = parseInt(this.getAttribute('min'));
            let value = parseInt(this.value);

            if (value > max) {
                this.value = max;
                alert(`Maximum quantity available is ${max}`);
            } else if (value < min) {
                this.value = min;
            }
        });
    });

    // Confirmation Dialogs for Delete Actions
    const deleteButtons = document.querySelectorAll('a[href*="delete"], button[type="submit"][onclick*="confirm"]');
    deleteButtons.forEach(button => {
        if (!button.onclick) {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Cart Quantity Update
    const cartQuantityInputs = document.querySelectorAll('.cart-quantity');
    cartQuantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const newQuantity = parseInt(this.value);
            
            if (newQuantity <= 0) {
                if (confirm('Remove this item from cart?')) {
                    // Redirect to remove URL
                    window.location.href = `/ecommerce/cart/remove/${itemId}/`;
                } else {
                    this.value = 1;
                }
            }
        });
    });

    // Image Preview for Product Forms
    const imageInputs = document.querySelectorAll('input[type="file"][name="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Create or update preview
                    let preview = document.getElementById('image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'image-preview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Price Formatting
    const priceElements = document.querySelectorAll('.price');
    priceElements.forEach(element => {
        const price = parseFloat(element.textContent.replace('$', ''));
        element.textContent = '$' + price.toFixed(2);
    });
});

// Utility Functions
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Add to Cart with AJAX (optional enhancement)
function addToCartAjax(productId, quantity) {
    // This can be enhanced with AJAX calls if needed
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/ecommerce/cart/add/${productId}/`;
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);
    
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

