const sair = document.querySelector('.btn-sair')
sair.addEventListener('click', function(event){
    if(confirm('Deseja mesmo sair?')){
        return true;
    }else{
        event.preventDefault();
    }})