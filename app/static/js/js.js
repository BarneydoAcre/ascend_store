//btn - shop_car_delete
let btnAdd = document.querySelectorAll('.btn-add-shop-car')
if(btnAdd){
    for(let i = 0; i < btnAdd.length; i++){
         btnAdd[i].addEventListener('click', function(event){
            if(confirm('Deseja mesmo apagar este dado?')){
                return true;
            }else{
                event.preventDefault();
            }
        });
}}