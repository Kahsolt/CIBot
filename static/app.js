/*
 * Main App Object
 *
 * Author : kahsolt
 * Update Date : 2018-01-12
 *
 */
var app = {};
var initApp = function () {

  /*
   * Section 1: UI
   */
  app.ui = {};

  app.ui.switchMenu = function (status) {
    if (status == true) {
      $('#menuUnlogin').hide();
      $('#menuLogin').show();
    } else {
      $('#menuLogin').hide();
      $('#menuUnlogin').show();
    }
  };
  app.ui.openMenu = function (evt, menuName) {
    $('#' + menuName).toggleClass('w3-show').prev().toggleClass('w3-light-blue');
  };
  app.ui.openTab = function (evt, tabName) {
    if (tabName == 'tabRegister') {
      app.http.getTags();
    } else if (tabName == 'tabHome') {
      app.http.getUser();
    }

    $('.tabcontent').hide();
    $('.tablink').removeClass('w3-light-blue');
    $('#' + tabName).show();
    evt.currentTarget.className += " w3-light-blue";
  };
  app.ui.openNotice = function (msg, level) {
    $('#msgNotice p:first').text(msg);
    var notice = $('#msgNotice');
    if (level == 'INFO') {
      notice.removeClass("w3-red").removeClass("w3-green").addClass("w3-blue");
    } else if (level == 'SUCCESS') {
      notice.removeClass("w3-red").removeClass("w3-blue").addClass("w3-green");
    } else {
      notice.removeClass("w3-green").removeClass("w3-blue").addClass("w3-red");
    }
    notice.show().fadeOut(5500);
  };
  app.ui.openTaskModal = function () {
    alert('TODO: 替换任务框内容为Pool选中的条目');
    $('#modalTask').show();
  };
  app.ui.addChatQuestion = function (msg) {
    $('#divChatConsole').append($('<div>').addClass('w3-opacity').addClass('w3-container').addClass('w3-right-align').text(msg));
  };
  app.ui.addChatAnswer = function (msg) {
    $('#divChatConsole').append($('<div>').addClass('w3-opacity').addClass('w3-container').text(msg));
  };
  app.ui.addTaskPool = function (task) {
    alert('TODO: 增加一个任务到Pool');
  };

  /*
   * Section 2: HTTP Server
   */
  app.http = {};
  app.http.SERVER_BASE = 'http://127.0.0.1:8000/';

  app.http.login = function () {
    var data = {
      username: $('div[id=formLogin] input[name=username]').val()
    };
    $.post(app.http.SERVER_BASE + 'user/login', JSON.stringify(data),
      function (resp) {
        if (resp['errorno'] == 200) {
          app.ui.switchMenu(true);
          app.ui.openNotice('登录成功 :)', 'SUCCESS');
          app.ui.openTab(event, 'tabHome');
        } else {
          app.ui.openNotice('登录失败 X(', 'ERROR');
          console.log('[login] ' + JSON.stringify(resp));
        }
      }, "json");
  };
  app.http.logout = function () {
    if (confirm('真的要退出吗？')) {
      var data = {};
      $.post(app.http.SERVER_BASE + 'user/logout', JSON.stringify(data),
        function (resp) {
          app.client.USER = null;
          app.ui.switchMenu(false);
          app.ui.openNotice('注销成功！', 'SUCCESS');
          app.ui.openTab(event, 'tabLogin');
        }, "json");
    }
  };
  app.http.register = function () {
/*
    var tags = [];
    $('input[type=checkbox]:checked').each(function () {
      tags.push($(this).val());
    });

    var data = {
      username: $('div[id=formRegister] input[name=username]').val(),
      tags: tags
    };
*/
    var data = {
      username: $('div[id=formRegister] input[name=username]').val(),
      tags: $('div[id=formRegister] input[name=tags]').val()
    };

    $.post(app.http.SERVER_BASE + 'user/register', JSON.stringify(data),
      function (resp) {
        if (resp['errorno'] == 200) {
          app.ui.openNotice('注册成功！', 'SUCCESS');
          app.ui.openTab(event, 'tabLogin');
        } else {
          app.ui.openNotice('注册失败……', 'ERROR');
          console.log('[register] ' + JSON.stringify(resp));
        }
      }, "json");
  };
  app.http.keepalive = function () {
    $.post(app.http.SERVER_BASE + 'user/keepalive', JSON.stringify({}),
      function (resp) {
        app.ui.switchMenu(resp['errorno'] == 200);
      }, "json");
  };
  app.http.getTags = function () {
    $('#pTags>:gt(1)').remove();
    $.get(app.http.SERVER_BASE + 'tag',
      function (resp) {
        var i, tags = resp['tags'];
        var $pTags = $('#pTags');
        for (i = 0; i < tags.length; i++) {
          $pTags.append($('<label>').addClass('tag').text(tags[i]).append($('<input>').attr('type', 'checkbox').attr('value', tags[i]).addClass('w3-check')));
          if (i % 4 == 3) $pTags.append($('<br>')); // 每行四个
        }
      }, "json");
  };
  app.http.getUser = function () {
    $.get(app.http.SERVER_BASE + 'user',
      function (resp) {
        app.client.USER = resp;
        console.log('[getUser] ' + JSON.stringify(resp));
        app.client.refreshHome();
      }, "json");
  };
  app.http.question = function () {
    var quest = $('#formQuestion>input[type=text]').val();
    app.ui.addChatQuestion(quest);
    var data = {
      'uid': app.client.USER && app.client.USER['id'] || 0,
      'question': quest
    };
    $.post(app.http.SERVER_BASE + 'q', JSON.stringify(data),
      function (resp) {
        app.ui.addChatAnswer(resp['answer']);
        console.log('[question] ' + JSON.stringify(resp))
      }, "json");
  };
  app.http.answer = function () {
    alert('Ne faris ankoraux!!!');
  };

  /*
   * Section 3: Client Cache
   */
  app.client = {};
  app.client.USER = null;

  app.client.refreshHome = function () {
    var $info = $('#divUserinfo');
    $info.empty();
    $info.append($('<p>').text('用户名: ' + app.client.USER['username']))
      .append($('<p>').text('兴趣列表: '));
    var $ul = $('<ul>').addClass('w3-ul');
    var i;
    for (i = 0; i < app.client.USER['tags'].length; i++) {
      $ul.append($('<li>').text(app.client.USER['tags'][i]));
    }
    $info.append($ul);
  };

}();

/*
 * Main Entry
 */
app.http.keepalive();
