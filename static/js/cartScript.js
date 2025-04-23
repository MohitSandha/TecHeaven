document.querySelectorAll('.quantity-controls').forEach(control => {
    const productId = control.dataset.productId;
    const quantitySpan = control.querySelector('.quantity');

    control.querySelector('.btn-plus').addEventListener('click', () => {
        updateQuantity(productId, 'increase', quantitySpan);
    });

    control.querySelector('.btn-minus').addEventListener('click', () => {
        updateQuantity(productId, 'decrease', quantitySpan);
    });
});

function updateQuantity(productId, action, quantitySpan) {
    fetch('/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId, action: action })
    })
    .then(response => response.json())
    .then(data => {
        // Update the quantity for the product
        quantitySpan.textContent = data.new_quantity;

        // Update the cart summary
        document.getElementById('cart-quantity').textContent = data.total_items;
        document.getElementById('subtotal').textContent = `£${data.subtotal.toFixed(2)}`;
        document.getElementById('delivery').textContent = `£${data.delivery_cost.toFixed(2)}`;
        document.getElementById('total').textContent = `£${data.total.toFixed(2)}`;
    });
}


// script.js
// Reference to the modal and its buttons
const confirmDeleteModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');

// Track the product ID to delete
let productToDeleteId = null;

// Set product ID when a delete button is clicked
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
        productToDeleteId = this.getAttribute('data-product-id');
    });
});

// Handle the "Delete" action
confirmDeleteBtn.addEventListener('click', () => {
    if (productToDeleteId) {
        fetch(`/delete_product/${productToDeleteId}`, {
            method: 'POST',  // Changed from DELETE to POST
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({})  // Optional body, some setups require it
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove product from DOM
                const productDiv = document.querySelector(`[data-product-id='${productToDeleteId}']`).closest('.container-fluid');
                if (productDiv) {
                    productDiv.remove();
                }

                // Hide modal using Bootstrap 5 API
                confirmDeleteModal.hide();

                // Clear the ID for safety
                productToDeleteId = null;
            } else {
                alert('Failed to delete the product.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
});