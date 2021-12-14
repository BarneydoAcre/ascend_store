// (function(win,doc){
//     'use strict';

//     if(document.querySelector('.btn-add-shop-car')){
//         let form = document.querySelector('.btn-add-shop-car')
//         function sendForm(event){
//             event.preventDefault();
//             let data = new FormData(form)
//             let ajax = new XMLHttpRequest();
//             let token = doc.querySelectorAll('input')[0].value;
//             ajax.open('POST', form.action);
//             ajax.setRequestHeader('X-CSRF-TOKEN',token);
//             ajax.onreadystatechange = function()
//             {
//                 if(ajax.status === 200 && ajax.readyState === 4){
//                     let result = doc.querySelector('#result');
//                     result.innerHTML = 'Operação realizada com sucesso!';
//                     result.classList.add('alert');
//                     result.classList.add('alert-success');
//                 }
//             }
//             ajax.send(data);
//             form.reset();
//         }
//         form.addEventListener('submit',sendForm,false);
//     }
// })(window,document);