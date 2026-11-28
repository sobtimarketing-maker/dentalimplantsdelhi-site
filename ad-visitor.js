/* Visitors who arrive from a Google ad see the clinic's Google-ad phone line
   (83682 22098), so the front desk can count ad calls. Everyone else, and
   every search engine, sees the usual number (87449 85976). The WhatsApp
   number never changes; only its opening line says "I saw your Google ad."
   The only thing stored is the time of the ad visit, kept for 7 days. */
(function () {
  var KEY = 'sdc_ad_visit';
  var DAYS = 7;
  var AD_CLICK = /[?&](gclid|gbraid|wbraid|gad_source)=/;

  function fromAd() {
    var tagged = AD_CLICK.test(location.search);
    try {
      if (tagged) {
        localStorage.setItem(KEY, String(Date.now()));
        return true;
      }
      var t = Number(localStorage.getItem(KEY));
      return t > 0 && Date.now() - t < DAYS * 864e5;
    } catch (e) {
      return tagged;
    }
  }

  var NUM = /87449([\s -]?)85976/g;
  function swapText(s) {
    return s.replace(NUM, '83682$122098');
  }

  function apply() {
    var links = document.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var h = a.getAttribute('href');
      if (h.indexOf('tel:') === 0 && h.replace(/\D/g, '').slice(-10) === '8744985976') {
        a.setAttribute('href', 'tel:+918368222098');
      } else if (h.indexOf('wa.me/') !== -1) {
        a.setAttribute('href', h.replace('I%20found%20you%20on%20Google.', 'I%20saw%20your%20Google%20ad.'));
      }
    }
    var labelled = document.querySelectorAll('[aria-label], [title]');
    for (var j = 0; j < labelled.length; j++) {
      var el = labelled[j];
      var names = ['aria-label', 'title'];
      for (var k = 0; k < names.length; k++) {
        var v = el.getAttribute(names[k]);
        if (v && NUM.test(v)) el.setAttribute(names[k], swapText(v));
        NUM.lastIndex = 0;
      }
    }
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode && n.parentNode.nodeName;
        return p === 'SCRIPT' || p === 'STYLE' ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var node;
    while ((node = walker.nextNode())) {
      NUM.lastIndex = 0;
      if (NUM.test(node.nodeValue)) node.nodeValue = swapText(node.nodeValue);
    }
    NUM.lastIndex = 0;
  }

  if (!fromAd()) return;
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', apply);
  } else {
    apply();
  }
})();
