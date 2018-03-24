$(document).ready(() => {
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
});
