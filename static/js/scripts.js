/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

function setActiveCategory(event, categoryName) {
    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(button => button.classList.remove('active'));

    // Add active class to the clicked button
    event.target.classList.add('active');

    // Set the selected category value in the h5 element
    document.getElementById('selected_category').textContent = categoryName + ' Menu';
  }
  function setVariant(event, id) {
    console.log(id)
  const variants = document.querySelectorAll('.product_variant'); // Select all elements with the 'product_variant' class

  // Loop through all variants
  variants.forEach(variant => {
    // Check if the 'data-id' of the variant matches the passed 'id'
    if (variant.dataset.id == id) {
      variant.classList.remove('d-none'); // Remove 'd-none' class to show the element
    } else {
      variant.classList.add('d-none'); // Add 'd-none' class to hide the element
    }
  });
}