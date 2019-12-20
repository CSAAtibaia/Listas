let saldo
let preco
let campo_preco
let campo_saldo
let quantidade
let campo_prod
let pk
let url

$(document).on('change', '.clProduto', function() {
  pk = $(this).val();
  // Aqui é feito o cálculo de subtração do estoque
  // saldo = Number(estoque) - Number(quantidade);
  campo_saldo = $(this).attr('id').replace('produto', 'saldo')

  url = '/produto/' + pk + '/json/'

  $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
      saldo = response.data[0].saldo
    },
    error: function(xhr) {
      // body...
    }
  })

  $('#'+campo_saldo).val(saldo)
});