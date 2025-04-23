
document.querySelectorAll('.addToCartbtn').forEach(button => {
    button.addEventListener('click', () => {
        const productId = button.getAttribute('data-product-id');

        fetch('/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Product added to cart!");
            } else {
                alert("Please login to add products.");
            }
        });
    });
});
// Fetch the rating value from the label with id "averageRating"
const rating = parseFloat(document.getElementById('averageRating').innerText);

// Function to update progress bars based on the rating
function setRating(rating) {
    // Set the label with the rating
    document.getElementById('averageRating').innerText = rating.toFixed(1); // Ensure 1 decimal place

    // Full progress bars based on the integer part of the rating
    document.getElementById('star5').value = (rating >= 5) ? 100 : 0;
    document.getElementById('star4').value = (rating >= 4) ? 100 : 0;
    document.getElementById('star3').value = (rating >= 3) ? 100 : 0;
    document.getElementById('star2').value = (rating >= 2) ? 100 : 0;
    document.getElementById('star1').value = (rating >= 1) ? 100 : 0;

    // Handle fractional part of the rating
    let fractionalPart = (rating % 1) * 100; // This will be the percentage for the last bar
    
    if (rating >= 4.5) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 50; // Full 4th star
        document.getElementById('star3').value = 100; // Full 3rd star
        document.getElementById('star2').value = 100; // Full 2nd star
        document.getElementById('star1').value = 100; // Full 1st star
    } else if (rating >= 4) {
        document.getElementById('star5').value = 0; // Full 5th star
        
    } else if (rating >= 3.5) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 0; // Full 4th star
        document.getElementById('star3').value = fractionalPart; // Partial 3rd star
    } else if (rating >= 3) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 0; // Full 4th star
       
    } else if (rating >= 2.5) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 0; // Full 5th star
        document.getElementById('star3').value = fractionalPart; // Partial 4th star
    } else if (rating >= 2) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 0; // Full 4th star
        document.getElementById('star3').value = 0; // Full 5th star
    } else if (rating >= 1.5) {
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star4').value = 0; // Full 5th star
        document.getElementById('star3').value = 0; // Full 5th star
        document.getElementById('star2').value = fractionalPart; // Partial 5th star
    } else if (rating >= 1) {
        document.getElementById('star1').value = 100; // Full 1st star
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star5').value = 0; // Full 5th star
        document.getElementById('star5').value = 0; // Full 5th star
    } else {
        document.getElementById('star5').value = 0;  // Empty all stars
    }
}

// Call the function to update progress bars based on the rating
setRating(3);