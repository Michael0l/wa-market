var btnSearch = document.querySelector('.search__txt');
var products = document.querySelectorAll(".box_product");
var btnCategory = document.querySelectorAll('.category__btn');
var productPlus = document.querySelectorAll('.product_plus');
var productMinus = document.querySelectorAll('.product_minus');
var basketBtn = document.querySelector('.btn_basket');
var basketWindow = document.querySelector('.basket_wrapper');
var basketScroll = document.querySelector('.basket_window');
var header = document.querySelector('.header');
var productsBox = document.querySelector('.products');
var closeBasket = document.querySelector('.title_basket');
var underBasket = document.querySelector('.under_basket');
var cartItemTemplate = document.querySelector('#product_basket');
var basketBox = document.querySelector('.basket_window');
var cartTotalPrice = document.querySelector('.total_price');
var submit = document.querySelector('.submit');

Telegram.WebApp.ready();

function print(a){
    console.log(a)
}

basketBtn.addEventListener('click', activeBasket)
closeBasket.addEventListener('click', activeBasket)


function activeBasket() {
    basketWindow.classList.toggle('active');
    basketScroll.classList.toggle('active');
    underBasket.classList.toggle('active');
    header.classList.toggle('hide');
    productsBox.classList.toggle('hide');
    basketBtn.classList.toggle('hide');
}



function search() {
    let input = document.querySelector(".search__txt");
    let filter = input.value.toUpperCase();
    for (let i = 0; i < products.length; i++) {
        let a = products[i].querySelector(".product_name");
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            products[i].style.display = "";
        } else {
            products[i].style.display = "none";
        }
    }
}

btnSearch.addEventListener('keyup', search);





function filter (category, items) {
    items.forEach((item) => {
        const isItemFiltered = item.dataset.category_id
        const isShowAll = category.toLowerCase() === 'all'
        if (isItemFiltered && !isShowAll) {
            item.classList.add('hide')
            } else {
            item.classList.remove('hide')
        }
        if (category === isItemFiltered) {
            item.classList.remove('hide')
        }
    })
} 

btnCategory.forEach((button) => {
    button.addEventListener('click', () => {
        btnCategory.forEach((item) => {
            item.classList.remove('category_active')
        })
        button.classList.add('category_active')
        const currentCategory = button.dataset.category;
        filter(currentCategory, products);
    })
})


// Устанавливаем обработчики

productPlus.forEach((item) => {
    parentBox = item.closest('.box_product');
    var productId = parentBox.dataset.product_id;

    item.addEventListener('click', () => addProductCart(productId))
})


productMinus.forEach((item) => {
    parentBox = item.closest('.box_product');
    var productId = parentBox.dataset.product_id;
    item.addEventListener('click', () => removeProductCart(productId))
})


// Получаем данные из LocalStorage
function getCartData(){
    return JSON.parse(sessionStorage.getItem('cart'));
}
// Записываем данные в LocalStorage
function setCartData(o){
    sessionStorage.setItem('cart', JSON.stringify(o));
    return false;
}



// Добавляем товар в корзину
function addProductCart(productId){
    var parentBox = productsBox.querySelector(`[data-product_id="${productId}"]`) // Главная карточка товара
    var cartData = getCartData() || {}, // Получаем данные корзины
        productBasket = getProduct(parentBox, productId),
        productTitle = parentBox.querySelector('.product_name').innerHTML, // название товара
        productPrice = parentBox.querySelector('.product_cost').innerHTML, // стоимость товара
        // productImg = parentBox.querySelector('.product_img').getAttribute('src');  // изображение товара
        btnMinus = parentBox.querySelector('.product_minus'),
        productCount = parentBox.querySelector('.product_count'),
        productBasketCount = productBasket.querySelector('.basket_count')
    if(cartData.hasOwnProperty(productId)){ //Если товар есть в корзине
        productCount.innerHTML = parseInt(productCount.innerHTML) + 1
        productBasketCount.innerHTML = productCount.innerHTML
        cartData[productId][2] += 1;
    } else { // Если товара нет
        btnMinus.classList.toggle("active");
        productCount.classList.toggle("active");
        productCount.innerHTML = '1'
        cartData[productId] = [productTitle, productPrice.split(' ').slice(0,-1).join('') , 1]
    }
    // Обновляем данные в LocalStorage
    setCartData(cartData)
    updateTotalPrice()
}








// Обработчик события на "Минус"

function removeProductCart(productId){
    print(productId)
    var parentBox = productsBox.querySelector(`[data-product_id="${productId}"]`) // Главная карточка товара
    var cartData = getCartData() || {}, // Получаем данные корзины
        productBasket = getProduct(parentBox, productId),
        btnMinus = parentBox.querySelector('.product_minus'),
        productCount = parentBox.querySelector('.product_count'),
        productBasketCount = productBasket.querySelector('.basket_count')

    if(cartData[productId][2] > 1){ //Если товар есть в корзине
        productCount.innerHTML = parseInt(productCount.innerHTML) - 1
        productBasketCount.innerHTML = productCount.innerHTML
        cartData[productId][2] -= 1;
    } else { // Если значение товара 1
        btnMinus.classList.toggle("active");
        productCount.classList.toggle("active");
        delete cartData[productId]
        productBasket.remove();
    }
    // Обновляем данные в LocalStorage
    setCartData(cartData)
    updateTotalPrice()
}



function createProductBasket(product, productId) {
    const productBasketTemplate = cartItemTemplate.content.cloneNode(true);
    const name = product.querySelector('.product_name');
    const nameTemplate = productBasketTemplate.querySelector('.product_name');
    nameTemplate.textContent = name.textContent

    const countTemplate = productBasketTemplate.querySelector('.basket_count');
    countTemplate.textContent = '1';

    const productText = product.querySelector('.product_text');
    const productTemplate = productBasketTemplate.querySelector('.product_text');
    productTemplate.textContent = productText.textContent;

    const image = product.querySelector('.product_img');
    const imageTemplate = productBasketTemplate.querySelector('.product_basket_img');
    imageTemplate.src = image.src;

    const productPrice = product.querySelector('.product_cost');
    const PriceTemplate = productBasketTemplate.querySelector('.product_cost');
    PriceTemplate.textContent = productPrice.textContent;

    productBasketTemplate.querySelector('.box_basket_product').dataset.product_id = productId.toString();
    return productBasketTemplate;
}


function getProduct(product, productId) {
    const existingCartItem = document.querySelector(`.box_basket_product[data-product_id="${productId}"]`);
    if (existingCartItem) {
        return existingCartItem;
    } else {
        let productBasket = createProductBasket(product, productId);
        basketBox.appendChild(productBasket);

        productBasket = basketBox.querySelector(`.box_basket_product[data-product_id="${productId}"]`);
        const productBasketAddButton = productBasket.querySelector('.product_basket_plus');
        productBasketAddButton.addEventListener('click', () => addProductCart(productId));

        const productBasketRemoveButton = productBasket.querySelector('.product_basket_minus');
        productBasketRemoveButton.addEventListener('click', () => removeProductCart(productId));
        return productBasket;
    }
}



function addProductListener(product, productId) {
    const cartItem = getProduct(product, productId);
    basketProductAddListener(product, cartItem);
}


function removeProductListener(product, productId) {
    const cartItem = getProduct(product, productId);
    cartItemRemoveListener(product, cartItem);
}


function basketProductAddListener(product, cartItem) {
    updateBasketProduct(product, cartItem);
    updateTotalPrice();
}



function updateBasketProduct(product, cartItem) {
    const productAmount = product.querySelector('.product_count');
    const productBasketAmount = cartItem.querySelector('.basket_count');
    productBasketAmount.textContent = productAmount.textContent;
}

function updateTotalPrice() {
    let total = 0;
    for (index = 1; index < basketBox.children.length; ++index) {
        amount = parseInt(basketBox.children[index].querySelector('.basket_count').textContent);
        total += parseInt(basketBox.children[index].querySelector('.product_cost').textContent.split(' ').slice(0, 2).join('')) * amount;
    }
    cartTotalPrice.textContent = total + ' ₽';
}


submit.addEventListener('click', submitClick)


function submitClick() {
    var data = getCartData()
    if(data.length != 0){
        fetch('/sendMessage', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            initData: window.Telegram.WebApp.initData,
            msg: data
        })
        });
    }

}