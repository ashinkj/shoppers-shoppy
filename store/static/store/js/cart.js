var updateBtns=document.getElementsByClassName("update-cart")

for(var i=0;i < updateBtns.length;i++){
    updateBtns[i].addEventListener("click",function(){
        var productId = this.dataset.product
        var action =this.dataset.action
        console.log('productId:',productId,'action:',action);
 
        console.log("USER:",user)
        if(user === 'AnonymousUser'){
            console.log("not logged in")
        }
        else{
            updateUserOrder(productId,action)
        }
    })

}

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
          location.reload()
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
          console.log('Response status:', response.status);
          console.log('Response text:', response.statusText);
          return response.text(); // Log the response content
        });
      
}