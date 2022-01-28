var inputPesquisa = document.querySelector(".inputPesquisa")

inputPesquisa.addEventListener('keyup', function() {
    inputPesquisaLink = document.querySelector(".inputPesquisaLink").href = "/?title="+inputPesquisa.value
    console.log(inputPesquisaLink.href)
})

console.log(inputPesquisa)