let USER_DATABASE = [
    {id:1, username:"erfan", password:"La160197",first_name:"Erfan", last_name:"Ezzati"},
    {id:2, username:"amir", password:"La160197",first_name:"falah", last_name:"amiri"},
    {id:3, username:"reza", password:"La160197",first_name:"reza", last_name:"golzar"},
    {id:4, username:"leito", password:"La160197",first_name:"Behzad", last_name:"Davarpanah"},
    {id:5, username:"hidden", password:"La160197",first_name:"Mehrad", last_name:"Hidden"},
]

let inputUsername = prompt("Enter Your Username")
let isInDatabase = USER_DATABASE.find(value=>value.username == inputUsername)
alert(isInDatabase?isInDatabase.password:"لطفا اول ثبت نام کنید")
