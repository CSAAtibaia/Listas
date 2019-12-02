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

  $('#add-item').click(function(ev) {
    ev.preventDefault();
    var count = $('#estoque').children().length;
    var tmplMarkup = $('#item-estoque').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    $('div#estoque').append(compiledTmpl);

    // update form count
    $('#id_estoque-TOTAL_FORMS').attr('value', count + 1);

    // Desabilita o campo 'Saldo'
    $('#id_estoque-' + (count) + '-saldo').prop('type', 'hidden')

    // some animate to scroll to view our new form
    $('html, body').animate({
      scrollTop: $("#add-item").position().top - 200
    }, 800);

    $('#id_estoque-' + (count) + '-produto').addClass('clProduto');
    $('#id_estoque-' + (count) + '-quantidade').addClass('clQuantidade');

    // Cria um span para mostrar o saldo na tela.
    $('label[for="id_estoque-' + (count) + '-saldo"]').append('<span id="id_estoque-' + (count) + '-saldo-span" class="lead" style="padding-left: 10px;"></span>')
    // Cria um campo com o estoque inicial.
    $('label[for="id_estoque-' + (count) + '-saldo"]').append('<input id="id_estoque-' + (count) + '-inicial" class="form-control" type="hidden" />')
    // Select2
    $('.clProduto').select2()
  });
