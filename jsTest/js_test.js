let products = [
    {id:1, name:"iphone 13 pro",price:205},
    {id:1, name:"iphone 13",price:105},
    {id:2, name:"iphone 15",price:175},
    {id:3, name:"iphone 12",price:155},
    {id:4, name:"iphone X",price:199},
    {id:5, name:"iphone 7",price:90},
    {id:6, name:"iphone 6",price:22},
]


let productsCart = [
    {id:1, name:"iphone X",price:199},
    {id:2, name:"iphone 7",price:90},
    {id:3, name:"iphone 6",price:22}
]

let allPrice = 0

let finalProductsCart = productsCart.filter((value)=>{
    return value.price < 100
})

productsCart.forEach((value, index, array)=>{
    allPrice += value.price
})

console.log(finalProductsCart.length);
console.log(allPrice+finalProductsCart.length);











// Remove from cart
// let products = [
//     {id:1, name:"iphone 13 pro",price:6000000},
//     {id:2, name:"iphone 15",price:5000000},
//     {id:3, name:"iphone 12",price:2800000},
//     {id:4, name:"iphone X",price:1000000},
//     {id:5, name:"iphone 7",price:100000},
//     {id:5, name:"iphone 6",price:10000},
// ]

// let productsCart = [
//     {id:4, name:"iphone X",price:1000000},
//     {id:5, name:"iphone 7",price:100000},
//     {id:5, name:"iphone 6",price:10000}
// ]
// let requestUser = prompt("Enter Number : \n 1: Add to cart \n 2: Delete from cart ")


// let deleteFromCart = (cart)=>{
//     let getName 
//     let indexProduct = -1
//     while(getName!="0"){
//         getName = prompt("Enter Your product for delete: \n if you don't want product enter 0").toLowerCase()
//         indexProduct = cart.findIndex(product=>product.name==getName)
//         if (indexProduct == -1){
//             alert("چنین محصولی در سبدخرید ندارید")
//         }
//         else{
//             cart.splice(indexProduct, 1)
//             console.table(cart);
//             break
//         }

//     }
// }

// if (requestUser === '2') {
//     deleteFromCart(productsCart)
// }



// let USER_DATABASE = [
//     {id:1, username:"erfan", password:"La160197",first_name:"Erfan", last_name:"Ezzati"},
//     {id:2, username:"amir", password:"La160197",first_name:"falah", last_name:"amiri"},
//     {id:3, username:"reza", password:"La160197",first_name:"reza", last_name:"golzar"},
//     {id:4, username:"leito", password:"La160197",first_name:"Behzad", last_name:"Davarpanah"},
//     {id:5, username:"hidden", password:"La160197",first_name:"Mehrad", last_name:"Hidden"},
// ]

// let inputUsername
// let inputPassword
// let getUser
// let isAuth = false

// // Authenticating
// while(isAuth == false){
//     inputUsername = prompt("Enter Your Username :")
//     inputPassword = prompt("Enter Your Password :")
//     USER_DATABASE.some((value)=>{
//         if(inputUsername == value.username && inputPassword == value.password){
//             isAuth = true
//         }
//     })
//     if(isAuth == false){
//         alert("Your Username or Password is incorrect")
//     }
//     }





//  product add to cart
// let products = [
//     {id:1, name:"iphone 13 pro",price:6000000},
//     {id:2, name:"iphone 15",price:5000000},
//     {id:3, name:"iphone 12",price:2800000},
//     {id:4, name:"iphone X",price:1000000}
// ]

// let requestUserProduct = ""
// let isInArray = false
// let productsCart = []
// let requestedProduct
// let id

// while(requestUserProduct!="0" ){
//     requestUserProduct = prompt("Enter Your product: \n if you don't want product enter 0")
//     if(requestUserProduct!="0"){
//         isInArray = products.some((value)=>{
//             if(value.name == requestUserProduct){
//                 requestedProduct = value
//                 return true
//             }
//         })
//         if(isInArray == false){
//             alert("این محصول موجود نیست")
//         }else{
//             if (productsCart.length === 0){
//                 id = 1
//             }
//             else{
//                 id = productsCart[productsCart.length-1].id + 1
//             }
//             productsCart.push({id:id, name:requestedProduct.name, price:requestedProduct.price})
//             console.table(productsCart)
//         }
//     }
// }

