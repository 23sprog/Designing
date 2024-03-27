
let lamp = document.querySelector('img')
let lampflag
let changeTurn = ()=>{
    if (lampflag) {
        lamp.setAttribute('src', 'img/off.png')
        lampflag = false
    }else{
        lamp.setAttribute('src', 'img/on.png')
        lampflag = true
    }

}


