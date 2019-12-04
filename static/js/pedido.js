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
  campo_preco = $(this).attr('id').replace('produto', 'preco')

  url = '/produto/' + pk + '/json/'

  $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
      saldo = response.data[0].saldo
      preco = response.data[0].preco
    },
    error: function(xhr) {
      // body...
    }
  })

  $('#'+campo_saldo).val(saldo)
  $('#'+campo_preco).val(preco)
});

$(document).on('change', '.clQuantidade', function() {
  quantidade = $(this).val();
  // Aqui é feito o cálculo de subtração do estoque
  // saldo = Number(estoque) - Number(quantidade);
  campo_saldo = $(this).attr('id').replace('quantidade', 'saldo')
  campo_prod = $(this).attr('id').replace('quantidade', 'produto')
  campo_preco = $(this).attr('id').replace('quantidade', 'preco')

  pk = $('#'+campo_prod).val()
  url = '/produto/' + pk + '/json/'

  $.ajax({
    url: url,
    type: 'GET',
    success: function(response) {
      saldo = response.data[0].saldo
      preco = response.data[0].preco
    },
    error: function(xhr) {
      // body...
    }
  })

  if (Number(saldo) < Number(quantidade)) {
    alert('O saldo não pode ser negativo.')
    // Atribui o saldo ao campo 'saldo'
    $(this).val(0)
    $('#'+campo_saldo).val(saldo)
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
    var count = $('#item').children().length;
    var tmplMarkup = $('#item').html();
    var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
    $('div#item').append(compiledTmpl);

    // update form count
    $('#id_item-TOTAL_FORMS').attr('value', count + 1);

    // Desabilita o campo 'Saldo'
    $('#id_item-' + (count) + '-saldo').prop('type', 'hidden')

    // some animate to scroll to view our new form
    $('html, body').animate({
      scrollTop: $("#add-item").position().top - 200
    }, 800);

    $('#id_item-' + (count) + '-produto').addClass('clProduto');
    $('#id_item-' + (count) + '-quantidade').addClass('clQuantidade');

    // Cria um span para mostrar o saldo na tela.
    $('label[for="id_item-' + (count) + '-saldo"]').append('<span id="id_item-' + (count) + '-saldo-span" class="lead" style="padding-left: 10px;"></span>')
    // Cria um campo com o estoque inicial.
    $('label[for="id_item-' + (count) + '-saldo"]').append('<input id="id_item-' + (count) + '-inicial" class="form-control" type="hidden" />')
    // Select2
    $('.clProduto').select2()
  });
