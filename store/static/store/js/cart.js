var updateBtns=document.getElementsByClassName("update-cart")
// var tryButtons = document.getElementsByClassName("try");

// // Function to be called when a "try" button is clicked
// function handleTryButtonClick(event) {
//   // You can also access any data attributes or other properties of the clicked element
//   var productId = this.dataset.product;

//   // Call your function or perform any action you want here
//   console.log("Button clicked! Product ID:", productId);
//   // Call your function here
//   // myFunction(productId, action);
//   myValue(productId)
// }

// // Add click event listeners to all "try" buttons
// for (var i = 0; i < tryButtons.length; i++) {
//   tryButtons[i].addEventListener("click", handleTryButtonClick);
// }

// Get all elements with the class "try"
var tryButtons = document.getElementsByClassName("try");

// Function to be called when a "try" button is clicked
function handleTryButtonClick(event) {
  // You can also access any data attributes or other properties of the clicked element
  var productId = this.dataset.product;

  // Call your function or perform any action you want here
  console.log("Button clicked! Product ID:", productId);
  
  // Call your function here
  myValue(productId);
}

// Add click event listeners to all "try" buttons
for (var i = 0; i < tryButtons.length; i++) {
  tryButtons[i].addEventListener("click", handleTryButtonClick);
}

function myValue(productId) {
  // Replace the URL with the actual API endpoint URL
  var url = '/';

  // Create a JSON object to send in the request body
  var data = { 'productId': productId };

  // Log the data being sent
  console.log('Data to send:', JSON.stringify(data));

  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken, // Ensure that 'csrftoken' is defined
      },
      body: JSON.stringify(data),
  })
  .then((response) => {
      if (!response.ok) {
          throw new Error('Network response was not ok. Status code: ' + response.status);
      }
      const contentType = response.headers.get('Content-Type');
      if (!contentType || !contentType.includes('application/json')) {
          throw new Error('Response is not JSON');
      }
      return response.json();
  })
  .then((data) => {
    console.log('Response:', data);

    // Insert the received data into the placeholders
    document.getElementById('productBrandPlaceholder').textContent = data.product_brand;
    document.getElementById('productCategoryPlaceholder').textContent = data.product_category;
    document.getElementById('productPricePlaceholder').textContent = data.product_price;
    document.getElementById('productdescriptionPlaceholder').textContent = data.product_description;
    var productImageElement = document.getElementById('productImage');
    productImageElement.style.backgroundImage = `url('${data.product_image}')`;

  })
  .catch((error) => {
    console.error('Error fetching data:', error);
    console.error('Error details:', error.message);
    // Handle the error here (e.g., display an error message)
 });
}


for(var i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action =this.dataset.action
        console.log('productId:',productId,'action:',action);
 
        console.log("USER:",user)
        if(user == 'AnonymousUser'){
            addCookieItem(productId,action)
            
        }
        else{
            updateUserOrder(productId,action)
            
        }
        // myValue(productId)
    })

}

function addCookieItem(productId,action){
  console.log('Not logged in..')

  if (action == 'add'){
    if(cart[productId]==undefined){
      cart[productId]={'quantity':1}
    
    }
    else{
      cart[productId]['quantity'] += 1
    }
  }
  if (action == 'remove'){
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0){
      console.log('remove item')
      delete cart[productId]
    }
  }
  console.log('cart:',cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  // location.reload()
}

// function myValue(productId) {
//   // Construct the URL based on the productId parameter
//   var url = '/';  // Replace with the actual API endpoint URL

//   // Create a JSON object to send in the request body
//   var data = { 'productId': productId };

//   // Log the data being sent
//   console.log('Data to send:', JSON.stringify(data));

//   fetch(url, {
//       method: 'POST',
//       headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': csrftoken,
//       },
//       body: JSON.stringify(data),
//   })
//   .then((response) => {
//       if (!response.ok) {
//           throw new Error('Network response was not ok. Status code: ' + response.status);
//       }
//       return response.json();
//   })
//   .then((data) => {
//       console.log('Response:', data);
//   })
//   .catch((error) => {
//     console.error('Error fetching data:', error);
//     console.error('Error details:', error.message);
//  });
// }


function updateUserOrder(productId,action){
    console.log('user is logged in')
    var url ='/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then((data) => {
          console.log('data:', data);
          // location.reload()
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
          console.log('Response status:', response.status);
          console.log('Response text:', response.statusText);
          return response.text(); // Log the response content
        });
      
}