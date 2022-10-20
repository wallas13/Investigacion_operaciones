
document.addEventListener('DOMContentLoaded', () => {


    // submitting the form
    document.querySelector("#form-data").addEventListener('submit', onsubmit);

    // This event enable or disable the button
    document.querySelector("#form-data").addEventListener('keyup', toggleButton);

})

function toggleButton() {

    let toggle = true;

    document.querySelectorAll(".validate").forEach(elem => {
        if (elem.value == null || elem.value == "") {
            toggle = false;
        }
    });

    if(toggle){
        document.querySelector("#btnSent").disabled = false;
    }else{
        document.querySelector("#btnSent").disabled = true;
    }
}

function sent(data) {
    const request = new XMLHttpRequest();

    request.open('POST', 'http://127.0.0.1:5000/grafico')

    request.onload = (data) => {
        console.log(data);
    }

    const d = new FormData();
    d.append("MinMax", data["Minmax"]);
    d.append("Fo", JSON.stringify(data["Funcion objetivo"]));
    d.append("Restr", JSON.stringify(data["Restricciones"]));

    request.send(d)
}

function onsubmit(event) {

    //event.preventDefault();

    data = {
        "Minmax": document.querySelector("#minmax").value,
        "Funcion objetivo": getFuncionObjetivo(),
        "Restricciones": getRestricciones()
    }
    
    document.querySelector("#hiddenInput").value = JSON.stringify(data)
    //sent(data)

    return true;
}

function getFuncionObjetivo() {

    // Get the elements
    const inputs = document.querySelectorAll(".objFuncion");

    const f = {}

    for(i=0; i<inputs.length; i++){
        if (inputs[i]==null) inputs[0].classList.add('danger')
        else f[('x' + (i+1).toString())] = toDecimal(inputs[i].value);
    }

    return f;
}


function getRestricciones() {

    const restricciones = [];

    const resFields = document.querySelectorAll(".Restricciones");

    resFields.forEach(elem => {
        let variables = elem.querySelectorAll(".restric-var");
        let data = {}

        for(let i=0; i<variables.length; i++){
            let key = 'x' + (i+1).toString();
            let nameVar = '.res' + key;
            data[key] = toDecimal(elem.querySelector(nameVar).value)
        }

        data["op"] = elem.querySelector(".resOperand").value;
        data["result"] = toDecimal(elem.querySelector(".resResult").value);

        restricciones.push(data)
    });

    return restricciones;

}

function toDecimal(frac){

    let total = frac;
    if (frac.search("/") != -1){
        const numbers = frac.split("/");
        total = parseFloat(numbers[0]) / parseFloat(numbers[1]);
    }
    
    return total
}