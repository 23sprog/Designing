let getMinutes = Number(prompt("Enter Minutes : "))
let getSeconds = Number(prompt("Enter Seconds : "))
let timer

if ((Boolean(getSeconds) && getSeconds>0) && ((Boolean(getMinutes) || getMinutes>=0))) {
        timer = setInterval(()=>{
            getSeconds-=1;
            if(getSeconds === -1){
                getMinutes--;
                getSeconds = 59
            }
            if(getSeconds === 0 && getMinutes === 0){
                clearInterval(timer)
            }

            console.log(`${String(getMinutes)}:${String(getSeconds)}`);
    },1000)
}else{
    alert("ثانیه باید بالای 0 و عدد باشد!")
}
