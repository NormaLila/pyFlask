$(document).ready(function () {
    window.setTimeout(function() {
       $(".alert").fadeTo(1000, 0).slideUp(1000, function(){
           $(this).remove(); 
       });
   }, 3000);
});


const btnDelete = document.querySelectorAll('.btn-eliminar')

if (btnDelete){
   const btnArray = Array.from(btnDelete);
   btnArray.forEach((btn)=>{
       btn.addEventListener('click', (e)=>{
           if(!confirm('Esta seguro de eliminarlo')){
               e.preventDefault();
           }
       });
   });
}

const btnGuardar = document.querySelectorAll('.btn-guardar')

if (btnGuardar){
   const btnArray = Array.from(btnGuardar);
   btnArray.forEach((btn)=>{
       btn.addEventListener('click', (e)=>{
           if(!confirm('¿Esta seguro de grabar los datos?')){
               e.preventDefault();
           }
       });
   });
}