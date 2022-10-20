window.addEventListener('load', () => {
    validateMethod();
})

let left = 4;
let right = 1;

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector(".input-ecuaciones i:nth-child(2)").addEventListener("click", ()=>sumEcuaciones(true)); 
    document.querySelector(".input-ecuaciones i:nth-child(3)").addEventListener("click", ()=>resEcuaciones(true));
    
    document.querySelector(".input-variables i:nth-child(2)").addEventListener("click", ()=>sumEcuaciones(false));
    document.querySelector(".input-variables i:nth-child(3)").addEventListener("click", ()=>resEcuaciones(false));
    
    const select = document.querySelector("select");
    select.value = "metodoGrafico";
    select.addEventListener("click", validateMethod);
    validateMethod();

    document.querySelector(".btn-left").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(left < 4 && left > 0){
            selected.style.marginLeft = `${(selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) + 100}%`;
            left++;
            right--;
        }       
    }

    document.querySelector(".btn-right").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(right < 4 && right > 0){
            selected.style.marginLeft =  `${(selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) - 100}%`;
            left--;
            right++;
        }
    }
});


const sumEcuaciones = (flag)=>{
    let input;
    if (flag) input =  document.getElementById("ecuaciones");
    else input = document.getElementById("variables");

    if (input.value == "") input.value = 1
    else input.value = (parseInt(input.value) + 1);
}

const resEcuaciones = (flag)=>{
    let input;
    if (flag) input = document.getElementById("ecuaciones")
    else input = document.getElementById("variables");

    if (input.value == "" || input.value == 1) input.value = 1
    else input.value = (parseInt(input.value) - 1);
}

const validateMethod = ()=>{
    const method = document.querySelector("select").value;
    const input = document.getElementById("variables");
    const i = document.querySelectorAll(".input-variables i");
    if (method == "metodoGrafico"){
        input.value = 2;
        input.setAttribute("readonly","true")
        for (element of i){
            element.style.display = "none";
        }
    }
    else{
        input.value = 1;
        input.removeAttribute("readonly")
        for (element of i){
            element.style.display = "block";
        }
    }
}
    
