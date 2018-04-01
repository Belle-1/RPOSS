// ordering logic
// binding events to functions
$(document.body).on('click', '.add-to-order', function(){  // adds clicked item to order
  var item_id = $(this).attr('data-id');
  var item_name = $(this).attr('data-name');
  var item_price = $(this).attr('data-price');
  var item_size = $(this).attr('data-size');
  var item_image = $(this).find('img').attr('src');

  addItemToOrder(item_id, item_name, item_price, item_size, 1, item_image);
  displayOrder();
});

$(document.body).on('click', '#clear-order', function(){  // clears order
  clearOrder();
  displayOrder();
});

$(document.body).on('click', '.remove-all-btn', function(){  // removes an item entirely from order
  var item_name = $(this).attr('data-name');
  removeItemFromOrderAll(item_name);
  displayOrder();
});

$(document.body).on('click', '.add-btn', function(){  // addes to item qty by 1
  var item_id = $(this).attr('data-id');
  var item_name = $(this).attr('data-name');
  var item_price = $(this).attr('data-price');
  var item_size = $(this).attr('data-size');
  var item_image = $(this).attr('src');
  addItemToOrder(item_id, item_name, item_price, item_size, 1, item_image);
  displayOrder();
});

$(document.body).on('click', '.remove-btn', function(){  // addes to item qty by 1
  var item_name = $(this).attr('data-name');
  removeItemFromOrder(item_name);
  displayOrder();
});













//
function displayOrder(){ // displaying selected menu items and their billing info on checkout1 section.
  var displayOrder = "";  //this is where all selected items will appear
  console.log(order);
  for (var i in order){
    var itemTotal = (order[i].item_price * order[i].item_qty)  // item_price * item_qty
    displayOrder += "<tr><th class='fit align-middle'><img src='" + order[i].item_image
      + "' class='img-responsive img-circle' width='75' height='75'></th><td class='align-middle'><span class='text-uppercase'>" + order[i].item_name
      + "</span><br>$" + order[i].item_price
      + "</td><td class='align-middle fit'><button data-name='" + order[i].item_name
      + "' class='btn-sm btn-outline-danger btn-circle text-danger remove-all-btn'>X</button></td><td class='align-middle fit'><button data-name='"  + order[i].item_name
      + "' class='btn-sm btn-outline-light btn-circle add-btn'>+</button></td><td class='align-middle text-center fit'>" + order[i].item_qty
      + "</td><td class='align-middle fit'><button data-name='"+ order[i].item_name
      + "' class='btn-sm btn-outline-light btn-circle remove-btn'>-</button></td><td class='align-middle fit text-right'>$"
      + Number(itemTotal).toFixed(2) + "</td></tr>"
  };

  $("#display-order").html(displayOrder);
  $("#my-order").html(" " + countOrder() + " ITEMS" + " ($" + totalAmount() + ")"); // shows items total qty + total amount
  $("#sub-deli-tax").html("$ " + subTotal() + "<br>" + "$ " + delivery_charges + "<br>" + "% " + delivery_taxes);  // shows bill info
  $("#total").html("$ " + totalAmount()); // shows total amount

  next();
};

var order = [];  // for storing order's items

var Item = function(item_id, item_name, item_price, item_size, item_qty, item_image){  // creates item instances
  this.item_id = item_id
  this.item_name = item_name
  this.item_price = item_price
  this.item_size = item_size
  this.item_qty = item_qty
  this.item_image = item_image
};

function addItemToOrder(item_id, item_name, item_price, item_size, item_qty, item_image){  // adds items to order array
  if (order === null){order = [];};

  for(var i in order){
    if(order[i].item_name === item_name){
      order[i].item_qty ++;
      saveOrder();
      return;
    };
  };
  var item = new Item(item_id, item_name, item_price, item_size, item_qty, item_image);
  order.push(item);
  saveOrder();
};

function removeItemFromOrder(item_name){  // removes item one qty down from order
  for(var i in order){
    if(order[i].item_name === item_name){
      order[i].item_qty --;
      if(order[i].item_qty === 0){
        order.splice(i, 1);
      };
      break;
    };
  };
  saveOrder();
};

function removeItemFromOrderAll(item_name){  // removes all item qty from order
  for(var i in order){
    if(order[i].item_name === item_name){
      order.splice(i, 1);
      break;
    };
  };
  saveOrder();
};

function clearOrder(){  // clears order array entirely
  order = [];
  saveOrder();
};

function countOrder(){  // returns total items qty
  var totalCount = 0;
  for(var i in order){
    totalCount += order[i].item_qty;
  };
  return totalCount;
};

function next(){
  if (order != null && max_amount > subTotal() && subTotal() > min_amount){
    $('.next').prop('disabled', false);  // enables Next button
  }else{
    $('.next').prop('disabled', true);  // disables Next button
  };
};

function subTotal(){  // returns order's total cost $
  var subTotal = 0;
  for(var i in order){
    subTotal += order[i].item_price * order[i].item_qty;
  };
  return Number(subTotal.toFixed(2));
};

function totalAmount(){  // returns the sum of totalCoset, delivery_charges and delivery_taxes
  var totalBeforTax = (subTotal() + delivery_charges);
  var taxes = totalBeforTax * (delivery_taxes / 100);
  var totalAfterTax = totalBeforTax + taxes ;
  return Number(totalAfterTax).toFixed(2)
};

function saveOrder(){  // saves order array on clicent side
  if(order === null){
    localStorage.setItem("order", JSON.stringify([]));
  }else{
    localStorage.setItem("order", JSON.stringify(order));
  };
};

function loadOrder(){  // returns order array from localStorage formated in JSON notation ready to be sende to the server
  order = JSON.parse(localStorage.getItem("order"));
  return order;
};

function removeOrder(){  // removes order from localStorage, this function is called once the order is submited to the server
  localStorage.removeItem("order");
};

loadOrder();
displayOrder();































//
