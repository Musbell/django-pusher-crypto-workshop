$(document).ready(() => {
  var LAST_PRICE;
  $('.js-price-' + window.APP_CONF.page.symbol).on('priceUpdated', function(evt, data){
    $('.js-buy-button').attr('disabled', false)
    LAST_PRICE = data.price;
  })

  var MY_ID;
  var pusher = pusherConnect()
  var channel = pusher.subscribe('presence-channel-' + window.APP_CONF.page.symbol);

  function addMember($members, idx, member){
      var $tr = $('<tr></tr>');
      $tr.data('member', idx)
      var $name = $('<td></td>');
      var $email = $('<td></td>');
      var $isUser;
      if(idx == MY_ID){
          $isUser = $('<th scope="row"><i class="fa fa-user"></i></th>');
      }else{
          $isUser = $('<td></td>');
      }

      $name.html(member.full_name)
      $email.html(member.email)
      $tr.append($name)
      $tr.append($email)
      $tr.append($isUser)

      $members.append($tr)
  }

  function buildMembersList(members){
      if(!MY_ID){
          MY_ID = members.myID;
      }
      var $members = $('.js-members');
      $members.html('');
      $.each(members.members, function(idx, member){
          addMember($members, idx, member);
      })
  }
  // Events
  channel.bind('pusher:subscription_succeeded', function(members) {
    buildMembersList(members)
  });
  channel.bind('pusher:member_added', function(member) {
      addMember($('.js-members'), member.id, member.info)
  });
  channel.bind('pusher:member_removed', function(member) {
      $('.js-members').find('tr').each(function(idx, elem){
          var $self = $(elem);
          if($self.data('member') == member.id){
              $self.remove()
          }
      })
  });
  channel.bind('operation', function(data){
    console.log(data)
    var $tr = $('<tr></tr>')
    var $isUser;
    var $user = $('<td class="user"></td>')
    var $amount = $('<td class="amount"></td>')
    var $price = $('<td class="price"></td>')
    var $time = $('<td class="time"></td>')

    if(data.user.id == MY_ID){
        $isUser = $('<th scope="row"><i class="fa fa-user"></i></th>');
    }else{
        $isUser = $('<th scope="row"></th>');
    }
    $user.html(data.user.full_name)
    $amount.html(data.amount)
    $price.html('USD ' + data.price)
    $time.html(data.timestamp)

    $tr.append($isUser)
    $tr.append($user)
    $tr.append($amount)
    $tr.append($price)
    $tr.append($time)

    $tr.prependTo(".js-transactions-table > .js-transactions-tbody");

  })

  // Ajax Setup
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", window.APP_CONF.csrfToken);
          }
      }
  });

  // Buy cryptos
  $('.js-buy-button').on('click', function(evt){
    if(!LAST_PRICE){
      return false;
    }
    var amount = $(this).data('amount')
    $.post(
      '/team/' + window.APP_CONF.page.symbol + '/buy', {
        amount: amount,
        price: LAST_PRICE
      }, function(data) {
        console.log(data)
      },
    "json");
  });
});
