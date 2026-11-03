/* Document Center list. Reads /documents.json; shows only entries with "on": true. Vanilla JS. */
(function () {
  var root = document.getElementById('list');
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }
  fetch('/documents.json').then(function (r) { return r.json(); }).then(function (d) {
    var banner = document.getElementById('banner');
    banner.className = 'banner';
    banner.setAttribute('role', 'note');
    var en = el('p', '', d.banner.en); en.lang = 'en';
    var th = el('p', '', d.banner.th); th.lang = 'th';
    banner.appendChild(en); banner.appendChild(th);
    var issuer = document.getElementById('issuer');
    issuer.textContent = d.entity.en + ' · ' + d.entity.th;
    d.businesses.forEach(function (b) {
      var docs = d.documents.filter(function (x) { return x.on === true && x.business === b.id; });
      if (!docs.length) return;
      root.appendChild(el('h2', 'biz', b.name));
      docs.forEach(function (x) {
        var c = el('div', 'doc');
        c.appendChild(el('h3', '', x.title_en));
        var t = el('p', 'th', x.title_th); t.lang = 'th'; c.appendChild(t);
        var btns = el('div', 'btns');
        var r = el('a', 'btn read', 'Read / อ่าน'); r.href = x.page;
        var p = el('a', 'btn pdf', 'Download PDF / ดาวน์โหลด PDF'); p.href = x.pdf; p.setAttribute('download', '');
        btns.appendChild(r); btns.appendChild(p); c.appendChild(btns); root.appendChild(c);
      });
    });
  }).catch(function () { root.appendChild(el('p', '', 'Could not load the list. / โหลดรายการไม่สำเร็จ')); });
})();
