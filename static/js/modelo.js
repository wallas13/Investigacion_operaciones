let left = 3;
let right = 1;

document.addEventListener('DOMContentLoaded', () => {

    const info_pages = document.querySelectorAll('.info-page');
    info_pages.forEach((elemento)=>{
        elemento.style.width = `calc( 100% / ${info_pages.length})`
    })
    const slider = document.querySelector('.slider');

    slider_pages = info_pages.length;
    left = slider_pages;
    slider.style.width = `${slider_pages}00%`;
    
    
    document.querySelector(".btn-left").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(left < slider_pages && left > 0){
            selected.style.marginLeft = `${(selected.style.marginLeft == "0%" || selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) + 100}%`;
            left++;
            right--;
        }       
    }

    document.querySelector(".btn-right").onclick = () =>{
        selected =  document.querySelector(".slider");
        if(right < slider_pages && right > 0){
            selected.style.marginLeft =  `${(selected.style.marginLeft == "" ? 0 : parseInt(selected.style.marginLeft)) - 100}%`;
            left--;
            right++;
        }
    }
   
});