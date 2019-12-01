let estoque
let campo_saldo
let quantidade
let campo_prod
let pk
let url

$(document).on('change', '.clQuantidade', function() {
  quantidade = $(this).val();
  // Aqui é feito o cálculo de subtração do estoque
  // saldo = Number(estoque) - Number(quantidade);
  campo_saldo = $(this).attr('id').replace('quantidade', 'saldo')
  campo_prod = $(this).attr('id').replace('quantidade', 'produto')
  pk = $('#'+campo_prod).val()
  url = '/produto/' + pk + '/json/'

  $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
      estoque = response.data[0].estoque
    },
    error: function(xhr) {
      // body...
    }
  })

  if (Number(estoque) < Number(quantidade)) {
    alert('O saldo não pode ser negativo.')
    // Atribui o saldo ao campo 'saldo'
    $(this).val(0)
    $('#'+campo_saldo).val(estoque)
    return
  }
  // Atribui o saldo ao campo 'saldo'
  x = $('#'+campo_saldo).val() - quantidade

  $('#'+campo_saldo).val(x)
  n = $('#id_pedido-credito').val() - quantidade
  $('#id_pedido-credito').val(n)
});