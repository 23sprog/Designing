let toDoListArray = [
    {id:1, name:"play piano", status:true},
    {id:2, name:"play video game", status:false},
    {id:3, name:"play football", status:false},
    {id:4, name:"start new project", status:false},
    {id:5, name:"start new project", status:false},
]

let addItem = (toDoList)=>{
    let toDoName = prompt("What is your to do list item : ")
    let id = 1
    if(!(toDoList.length===0)){
        id = toDoList.length + 1
    }
    toDoList.push({id:id, name:toDoName, status:false})
}

let checkItem = (toDoList)=>{
    let toDoName = prompt("What is your to do list item name: ")
    toDoList.forEach((value) => {
        if(value.name == toDoName){
            value.status = true
        }
    });
}



let deleteItem = (toDoList)=>{
    let toDoName = prompt("What is your to do list item : ")
    let itemIndex = -1
    itemIndex = toDoList.findIndex((value)=>{
        return toDoName == value.name
    })
    if(itemIndex == -1){
        alert("این آیتم وجود ندارد")
    }
    else{
        toDoList.splice(itemIndex, 1)
    }
}


let itemSelector = ''

while (itemSelector !== '-1') {
    if (itemSelector === '1') {
        addItem(toDoListArray)
        console.table(toDoListArray)    
    }
    else if(itemSelector === '2'){
        checkItem(toDoListArray)
        console.table(toDoListArray)
    }
    else if(itemSelector === '3'){
        deleteItem(toDoListArray)
        console.table(toDoListArray)
    }
    itemSelector = prompt("choose option :\n 1: add Item \n 2: checkItem \n 3: delete Item \n -1: Exit ")
}
