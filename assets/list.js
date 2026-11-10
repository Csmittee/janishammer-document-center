/* Document Center list. Reads /documents.json; shows only entries with "on": true. Vanilla JS.
   Per-business view: /?b=<business id> shows only that business, with its own banner and issuer line
   (a site or service links to ITS view, never to the full list at /). Changed: per-business view 2026-11-10 */
(function () {
  var root = document.getElementById('list');
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; }
  var wanted = new URLSearchParams(window.location.search).get('b');
  fetch('/documents.json').then(function (r) { return r.json(); }).then(function (d) {
    var businesses = d.businesses;
    var view = null;
    if (wanted) {
      businesses = d.businesses.filter(function (b) { return b.id === wanted; });
      view = businesses[0] || null;
      if (!view) {
        root.appendChild(el('p', '', 'No documents at this address. / ไม่พบเอกสารที่ที่อยู่นี้'));
        return;
      }
    }
    // banner and issuer: the business's own in a business view, else the global ones
    var b = (view && view.banner) || d.banner;
    var banner = document.getElementById('banner');
    banner.className = 'banner';
    banner.setAttribute('role', 'note');
    var en = el('p', '', b.en); en.lang = 'en';
    var th = el('p', '', b.th); th.lang = 'th';
    banner.appendChild(en); banner.appendChild(th);
    var issuer = document.getElementById('issuer');
    var ie = (view && view.issuer_en) || d.entity.en;
    var it = (view && view.issuer_th) || d.entity.th;
    issuer.textContent = ie + ' · ' + it;
    businesses.forEach(function (biz) {
      var docs = d.documents.filter(function (x) { return x.on === true && x.business === biz.id; });
      if (!docs.length) return;
      root.appendChild(el('h2', 'biz', biz.name));
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
