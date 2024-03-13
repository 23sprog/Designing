let USER_DATABASE = [
    {id:1, username:"erfan", password:"La160197",first_name:"Erfan", last_name:"Ezzati"},
    {id:2, username:"amir", password:"La160197",first_name:"falah", last_name:"amiri"},
    {id:3, username:"reza", password:"La160197",first_name:"reza", last_name:"golzar"},
    {id:4, username:"leito", password:"La160197",first_name:"Behzad", last_name:"Davarpanah"},
    {id:5, username:"hidden", password:"La160197",first_name:"Mehrad", last_name:"Hidden"},
]

let inputUsername
let inputPassword
let getUser
let isAuth = false

// Authenticating
while(isAuth == false){
    inputUsername = prompt("Enter Your Username :")
    inputPassword = prompt("Enter Your Password :")
    USER_DATABASE.some((value)=>{
        if(inputUsername == value.username && inputPassword == value.password){
            isAuth = true
        }
    })
    if(isAuth == false){
        alert("Your Username or Password is incorrect")
    }
    }