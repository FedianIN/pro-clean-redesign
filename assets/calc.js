/* Pro Clean price calculator.
   Prices and rules are copied from the calculator on pro-clean.es (Forminator form 2836):
   sofa = (48 + 9 per seat + shape + recliner 5) x material (leather 1.4)
   mattress = size x sides (2 sides 1.3) + headboard 28
   carpet = 8 per m2, chair = type price x qty, pillow = 5 each
   steam disinfection and fabric protector = +20% of the item
   special timing = +20 each, IVA 21%, discount on the total with IVA:
   5% from 100, 10% from 200, 15% from 300. Minimum order 40 with IVA. */
(() => {
  const root = document.getElementById('calc');
  const form = document.getElementById('quote-form');
  if (!root || !form) return;
  const lang = (document.documentElement.lang || 'en').slice(0, 2) === 'es' ? 'es' : 'en';

  const P = {
    sofa: { base: 48, seat: 9, recliner: 5,
      shape: { standard: 0, l: 4, u: 20, bed: 8, bedL: 12, bedU: 16 },
      material: { fabric: 1, leather: 1.4, other: 1 } },
    mattress: { size: { single: 40, double: 49, queen: 53.5, king: 62.5, pres: 68.5, head: 28 }, both: 1.3, headboard: 28 },
    carpet: { m2: 8 },
    chair: { armchair: 36, sun: 22, dining: 8, puff: 16, rocking: 17, baby: 17, reclining: 46, puffOut: 31 },
    pillow: 5,
    extra: 0.2, special: 20, iva: 0.21, min: 40,
    tiers: [[300, 15], [200, 10], [100, 5]],
  };

  const T = {
    en: {
      types: { sofa: 'Sofa', mattress: 'Mattress', carpet: 'Carpet or rug', chair: 'Chairs', pillow: 'Pillows' },
      legend: 'Build your estimate', pick: 'What do you want to clean?',
      shape: 'Shape', seats: 'Size', material: 'Material', recliner: 'Recliner sofa',
      shapes: { standard: 'Sofa', l: 'L shaped sofa', u: 'U shaped sofa', bed: 'Sofa bed', bedL: 'L shaped sofa bed', bedU: 'U shaped sofa bed' },
      seatN: (n) => `${n} seater`, materials: { fabric: 'Fabric', leather: 'Leather', other: 'Other' },
      size: 'Size', sizes: { single: 'Single, up to 105 × 200 cm', double: 'Double, up to 135 × 200 cm', queen: 'Queen, up to 150 × 200 cm', king: 'King, up to 180 × 210 cm', pres: 'Presidential king, up to 200 × 220 cm', head: 'Headboard only' },
      sides: 'Sides', side1: '1 side', side2: '2 sides', headboard: 'Also clean the headboard', sizeHint: 'Sizes are maximums. If your mattress is larger, choose the next size.',
      area: 'Area in m²', areaHint: 'Length × width. A 2 × 3 m rug is 6 m².',
      chairType: 'Type', chairs: { armchair: 'Armchair', sun: 'Sun lounger', dining: 'Dining chair', puff: 'Puff lounger', rocking: 'Rocking chair', baby: 'Baby carriage', reclining: 'Reclining chair', puffOut: 'Outdoor puff lounger' },
      qty: 'Quantity', steam: 'Extra steam disinfection', protector: 'Fabric protector', plus20: '+20%',
      add: 'Add to estimate', thisItem: 'This item', remove: 'Remove',
      list: 'Your items', empty: 'Add your first item to see the price.',
      special: 'Special timing', specials: ['Cleaning today', 'Early or late visit, 07:00 to 09:00 or 20:00 to 22:00', 'Weekend or public holiday'],
      specialHint: 'Depends on availability. If we cannot schedule it, the extra is not charged.',
      subtotal: 'Price without IVA', iva: 'IVA 21%', discount: (p) => `Discount ${p}%`, total: 'Estimated total',
      minNote: 'This is below our 40 € minimum order. Send it anyway, we may still be able to help.',
      estNote: 'Estimate based on our price list. We confirm the final price after seeing photos or the items.',
      errItems: 'Add at least one item, or describe the job in the notes.',
      msgHello: 'Hello Pro Clean, I would like to book a cleaning.', msgItems: 'Items', msgSpecial: 'Special timing',
      msgTotal: 'Estimated total', name: 'Name', town: 'Town', notes: 'Notes',
      missing: 'Some details are missing. Check the highlighted fields.', opening: 'Opening WhatsApp with your request.',
      seats_s: 'seats', m2: 'm²', both: 'both sides', withHead: 'with headboard',
    },
    es: {
      types: { sofa: 'Sofá', mattress: 'Colchón', carpet: 'Alfombra', chair: 'Sillas', pillow: 'Cojines' },
      legend: 'Calcula tu presupuesto', pick: '¿Qué quieres limpiar?',
      shape: 'Forma', seats: 'Tamaño', material: 'Material', recliner: 'Sofá reclinable',
      shapes: { standard: 'Sofá', l: 'Sofá en L', u: 'Sofá en U', bed: 'Sofá cama', bedL: 'Sofá cama en L', bedU: 'Sofá cama en U' },
      seatN: (n) => `${n} plazas`, materials: { fabric: 'Tela', leather: 'Piel', other: 'Otro' },
      size: 'Tamaño', sizes: { single: 'Individual, hasta 105 × 200 cm', double: 'Doble, hasta 135 × 200 cm', queen: 'Queen, hasta 150 × 200 cm', king: 'King, hasta 180 × 210 cm', pres: 'King presidencial, hasta 200 × 220 cm', head: 'Solo cabecero' },
      sides: 'Caras', side1: '1 cara', side2: '2 caras', headboard: 'Limpiar también el cabecero', sizeHint: 'Los tamaños son máximos. Si tu colchón es más grande, elige el siguiente.',
      area: 'Superficie en m²', areaHint: 'Largo × ancho. Una alfombra de 2 × 3 m tiene 6 m².',
      chairType: 'Tipo', chairs: { armchair: 'Sillón', sun: 'Tumbona', dining: 'Silla de comedor', puff: 'Puf tumbona', rocking: 'Mecedora', baby: 'Carrito de bebé', reclining: 'Sillón reclinable', puffOut: 'Puf tumbona exterior' },
      qty: 'Cantidad', steam: 'Desinfección extra con vapor', protector: 'Protector de tejidos', plus20: '+20%',
      add: 'Añadir al presupuesto', thisItem: 'Esta pieza', remove: 'Quitar',
      list: 'Tus piezas', empty: 'Añade tu primera pieza para ver el precio.',
      special: 'Horario especial', specials: ['Limpieza hoy', 'Visita temprano o tarde, de 07:00 a 09:00 o de 20:00 a 22:00', 'Fin de semana o festivo'],
      specialHint: 'Según disponibilidad. Si no podemos programarlo, no se cobra el extra.',
      subtotal: 'Precio sin IVA', iva: 'IVA 21%', discount: (p) => `Descuento ${p}%`, total: 'Total estimado',
      minNote: 'Está por debajo de nuestro pedido mínimo de 40 €. Envíalo igualmente, quizá podamos ayudarte.',
      estNote: 'Estimación según nuestra lista de precios. Confirmamos el precio final al ver fotos o las piezas.',
      errItems: 'Añade al menos una pieza o describe el trabajo en las notas.',
      msgHello: 'Hola Pro Clean, me gustaría reservar una limpieza.', msgItems: 'Piezas', msgSpecial: 'Horario especial',
      msgTotal: 'Total estimado', name: 'Nombre', town: 'Localidad', notes: 'Notas',
      missing: 'Faltan algunos datos. Revisa los campos marcados.', opening: 'Abriendo WhatsApp con tu solicitud.',
      seats_s: 'plazas', m2: 'm²', both: 'dos caras', withHead: 'con cabecero',
    },
  }[lang];

  const fmt = new Intl.NumberFormat(lang === 'es' ? 'es-ES' : 'en-IE', { style: 'currency', currency: 'EUR' });
  const money = (n) => fmt.format(Math.round(n * 100) / 100);
  const opt = (obj, labels, sel) => Object.keys(obj).map((k) => `<option value="${k}"${k === sel ? ' selected' : ''}>${labels[k]}</option>`).join('');
  const seg = (name, items, sel) => `<div class="seg" role="radiogroup">${items.map(([v, l]) =>
    `<label class="seg-opt"><input type="radio" name="${name}" value="${v}"${v === sel ? ' checked' : ''}><span class="body-5">${l}</span></label>`).join('')}</div>`;
  const check = (name, label, extra = '') => `<label class="check"><input type="checkbox" name="${name}"><span class="body-5">${label}</span>${extra ? `<span class="caption-2 muted">${extra}</span>` : ''}</label>`;
  const field = (label, inner, hint = '') => `<div class="cfield"><span class="caption-1">${label}</span>${inner}${hint ? `<span class="caption-2 muted">${hint}</span>` : ''}</div>`;

  const panels = {
    sofa: () => field(T.shape, `<select name="shape">${opt(P.sofa.shape, T.shapes, 'standard')}</select>`) +
      field(T.seats, `<select name="seats">${[2, 3, 4, 5, 6, 7, 8, 9].map((n) => `<option value="${n}"${n === 3 ? ' selected' : ''}>${T.seatN(n)}</option>`).join('')}</select>`) +
      field(T.material, seg('material', Object.keys(P.sofa.material).map((k) => [k, T.materials[k]]), 'fabric')) +
      `<div class="checks">${check('recliner', T.recliner, '+5 €')}${check('steam', T.steam, T.plus20)}${check('protector', T.protector, T.plus20)}</div>`,
    mattress: () => field(T.size, `<select name="size">${opt(P.mattress.size, T.sizes, 'double')}</select>`, T.sizeHint) +
      `<div data-show-unless-head>${field(T.sides, seg('sides', [['1', T.side1], ['2', T.side2]], '1'))}</div>` +
      `<div class="checks"><span data-show-unless-head>${check('headboard', T.headboard, '+28 €')}</span>${check('steam', T.steam, T.plus20)}</div>`,
    carpet: () => field(T.area, `<input type="number" name="area" min="0.5" max="200" step="0.5" value="4" inputmode="decimal">`, T.areaHint) +
      `<div class="checks">${check('steam', T.steam, T.plus20)}</div>`,
    chair: () => field(T.chairType, `<select name="chair">${opt(P.chair, T.chairs, 'dining')}</select>`) +
      field(T.qty, `<input type="number" name="qty" min="1" max="60" step="1" value="4" inputmode="numeric">`) +
      `<div class="checks">${check('steam', T.steam, T.plus20)}${check('protector', T.protector, T.plus20)}</div>`,
    pillow: () => field(T.qty, `<input type="number" name="qty" min="1" max="60" step="1" value="2" inputmode="numeric">`),
  };

  root.innerHTML = `
    <div class="calc-left">
    <fieldset class="calc-builder">
      <legend class="title-3">${T.legend}</legend>
      <span class="caption-1 calc-pick">${T.pick}</span>
      <div class="type-tabs" role="tablist">${Object.keys(T.types).map((k, i) =>
        `<button type="button" class="type-tab body-5${i ? '' : ' on'}" role="tab" aria-selected="${i ? 'false' : 'true'}" data-type="${k}"><i class="ph ph-${{ sofa: 'couch', mattress: 'bed', carpet: 'square-half-bottom', chair: 'chair', pillow: 'square' }[k]}"></i>${T.types[k]}</button>`).join('')}</div>
      <div class="type-panel" id="type-panel"></div>
      <div class="add-row">
        <p class="body-5"><span class="muted">${T.thisItem}</span> <strong id="item-price">0</strong> <span class="caption-2 muted">+ IVA</span></p>
        <button type="button" class="btn btn-light button-md" id="add-item"><i class="ph ph-plus"></i> ${T.add}</button>
      </div>
    </fieldset>
    <fieldset class="calc-special">
      <legend class="title-4">${T.special} <span class="caption-2 muted">+20 € ${lang === 'es' ? 'cada uno' : 'each'}</span></legend>
      <div class="checks">${T.specials.map((s, i) => check(`special${i}`, s)).join('')}</div>
      <span class="caption-2 muted">${T.specialHint}</span>
    </fieldset>
    </div>
    <div class="calc-right">
    <div class="calc-list">
      <p class="title-4">${T.list}</p>
      <ul id="item-list" class="item-list"></ul>
      <p class="empty caption-2" id="list-empty"><i class="ph ph-receipt"></i> ${T.empty}</p>
      <p class="field-error caption-2" id="items-error" role="alert" hidden>${T.errItems}</p>
    </div>
    <dl class="summary" id="summary" aria-live="polite"></dl>
    <p class="caption-2 calc-note" id="min-note" hidden>${T.minNote}</p>
    <p class="caption-2 calc-note muted">${T.estNote}</p>
    </div>`;
  const contact = form.querySelector('.calc-contact');
  if (contact) root.querySelector('.calc-right').appendChild(contact);

  const panel = root.querySelector('#type-panel');
  const priceEl = root.querySelector('#item-price');
  const listEl = root.querySelector('#item-list');
  const emptyEl = root.querySelector('#list-empty');
  const sumEl = root.querySelector('#summary');
  const minEl = root.querySelector('#min-note');
  const itemsErr = root.querySelector('#items-error');
  let type = 'sofa';
  const items = [];

  const val = (n) => panel.querySelector(`[name="${n}"]:checked, select[name="${n}"], input[type=number][name="${n}"]`)?.value;
  const on = (n) => !!panel.querySelector(`[name="${n}"]`)?.checked;
  const num = (n, min) => Math.max(min, parseFloat(String(val(n) || '0').replace(',', '.')) || 0);

  function current() {
    let price = 0; let label = '';
    const extras = [];
    if (type === 'sofa') {
      const shape = val('shape'); const seats = +val('seats'); const mat = val('material');
      price = (P.sofa.base + seats * P.sofa.seat + P.sofa.shape[shape] + (on('recliner') ? P.sofa.recliner : 0)) * P.sofa.material[mat];
      label = `${T.shapes[shape]}, ${T.seatN(seats)}, ${T.materials[mat].toLowerCase()}`;
      if (on('recliner')) extras.push(T.recliner.toLowerCase());
      const base = price; if (on('steam')) { price += base * P.extra; extras.push(T.steam.toLowerCase()); }
      if (on('protector')) { price += base * P.extra; extras.push(T.protector.toLowerCase()); }
    } else if (type === 'mattress') {
      const size = val('size'); const head = size === 'head';
      const sides = head ? 1 : +val('sides');
      price = P.mattress.size[size] * (sides === 2 ? P.mattress.both : 1) + (!head && on('headboard') ? P.mattress.headboard : 0);
      label = `${T.types.mattress}: ${T.sizes[size].split(',')[0]}`;
      if (sides === 2) extras.push(T.both);
      if (!head && on('headboard')) extras.push(T.withHead);
      if (on('steam')) { price += price * P.extra; extras.push(T.steam.toLowerCase()); }
    } else if (type === 'carpet') {
      const a = num('area', 0); price = a * P.carpet.m2;
      label = `${T.types.carpet}, ${String(a).replace('.', lang === 'es' ? ',' : '.')} ${T.m2}`;
      if (on('steam')) { price += price * P.extra; extras.push(T.steam.toLowerCase()); }
    } else if (type === 'chair') {
      const c = val('chair'); const q = Math.round(num('qty', 0));
      const base = P.chair[c] * q; price = base;
      label = `${T.chairs[c]} × ${q}`;
      if (on('steam')) { price += base * P.extra; extras.push(T.steam.toLowerCase()); }
      if (on('protector')) { price += base * P.extra; extras.push(T.protector.toLowerCase()); }
    } else if (type === 'pillow') {
      const q = Math.round(num('qty', 0)); price = q * P.pillow; label = `${T.types.pillow} × ${q}`;
    }
    return { price, label, extras };
  }

  function renderPanel() {
    panel.innerHTML = panels[type]();
    syncHead(); update();
  }
  function syncHead() {
    const head = type === 'mattress' && val('size') === 'head';
    panel.querySelectorAll('[data-show-unless-head]').forEach((el) => { el.hidden = head; });
  }
  function update() {
    const c = current();
    priceEl.textContent = money(c.price);
    root.querySelector('#add-item').disabled = !(c.price > 0);
  }

  function totals() {
    const items$ = items.reduce((s, it) => s + it.price, 0);
    const specials = [...root.querySelectorAll('.calc-special input:checked')].length * P.special;
    const sub = items$ + specials;
    const iva = sub * P.iva;
    const withIva = sub + iva;
    const tier = P.tiers.find(([from]) => withIva >= from);
    const pct = tier ? tier[1] : 0;
    const disc = withIva * pct / 100;
    return { sub, iva, pct, disc, total: withIva - disc, specials };
  }

  function renderList() {
    listEl.innerHTML = items.map((it, i) => `
      <li class="li-item">
        <div><p class="body-5">${it.label}</p>${it.extras.length ? `<p class="caption-2 muted">${it.extras.join(', ')}</p>` : ''}</div>
        <span class="body-5 li-price">${money(it.price)}</span>
        <button type="button" class="icon-btn" data-remove="${i}" aria-label="${T.remove}: ${it.label}"><i class="ph ph-x"></i></button>
      </li>`).join('');
    emptyEl.hidden = items.length > 0;
    renderSummary();
  }

  function renderSummary() {
    const t = totals();
    if (!items.length && !t.specials) { sumEl.innerHTML = ''; sumEl.hidden = true; minEl.hidden = true; return; }
    sumEl.hidden = false;
    sumEl.innerHTML = `
      <div><dt class="body-6">${T.subtotal}</dt><dd class="body-5">${money(t.sub)}</dd></div>
      <div><dt class="body-6">${T.iva}</dt><dd class="body-5">${money(t.iva)}</dd></div>
      ${t.pct ? `<div class="disc"><dt class="body-6">${T.discount(t.pct)}</dt><dd class="body-5">− ${money(t.disc)}</dd></div>` : ''}
      <div class="tot"><dt class="title-3">${T.total}</dt><dd class="heading-5">${money(t.total)}</dd></div>`;
    minEl.hidden = !(t.total > 0 && t.total < P.min);
  }

  root.querySelector('.type-tabs').addEventListener('click', (e) => {
    const b = e.target.closest('.type-tab'); if (!b) return;
    type = b.dataset.type;
    root.querySelectorAll('.type-tab').forEach((x) => { const sel = x === b; x.classList.toggle('on', sel); x.setAttribute('aria-selected', String(sel)); });
    renderPanel();
  });
  panel.addEventListener('input', () => { syncHead(); update(); });
  panel.addEventListener('change', () => { syncHead(); update(); });
  root.querySelector('#add-item').addEventListener('click', () => {
    const c = current(); if (!(c.price > 0)) return;
    items.push(c); itemsErr.hidden = true; renderList();
    const btn = root.querySelector('#add-item');
    btn.classList.add('added'); setTimeout(() => btn.classList.remove('added'), 600);
  });
  listEl.addEventListener('click', (e) => {
    const b = e.target.closest('[data-remove]'); if (!b) return;
    items.splice(+b.dataset.remove, 1); renderList();
  });
  root.querySelector('.calc-special').addEventListener('change', renderSummary);

  /* Submit: validate and open WhatsApp with the full estimate */
  const status = document.getElementById('form-status');
  const showErr = (el, show) => {
    el.classList.toggle('invalid', show); el.setAttribute('aria-invalid', String(show));
    const msg = el.closest('.field')?.querySelector('.field-error'); if (msg) msg.hidden = !show;
  };
  form.elements.name.addEventListener('input', (e) => { if (e.target.value.trim()) showErr(e.target, false); });
  form.elements.town.addEventListener('change', (e) => { if (e.target.value) showErr(e.target, false); });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = form.elements.name; const town = form.elements.town; const notes = form.elements.notes.value.trim();
    let ok = true;
    const hasWork = items.length > 0 || notes.length > 0;
    itemsErr.hidden = hasWork; if (!hasWork) ok = false;
    showErr(name, !name.value.trim()); if (!name.value.trim()) ok = false;
    showErr(town, !town.value); if (!town.value) ok = false;
    if (!ok) {
      status.textContent = T.missing;
      (form.querySelector('.invalid') || root.querySelector('.type-tab.on')).focus();
      return;
    }
    const t = totals();
    const specials = [...root.querySelectorAll('.calc-special input:checked')].map((i) => T.specials[+i.name.replace('special', '')]);
    const lines = [T.msgHello, ''];
    if (items.length) {
      lines.push(`${T.msgItems}:`);
      items.forEach((it) => lines.push(`• ${it.label}${it.extras.length ? ` (${it.extras.join(', ')})` : ''}: ${money(it.price)}`));
    }
    if (specials.length) lines.push('', `${T.msgSpecial}: ${specials.join(', ')}`);
    if (items.length || specials.length) {
      lines.push('', `${T.subtotal}: ${money(t.sub)}`, `${T.iva}: ${money(t.iva)}`);
      if (t.pct) lines.push(`${T.discount(t.pct)}: −${money(t.disc)}`);
      lines.push(`${T.msgTotal}: ${money(t.total)}`);
    }
    lines.push('', `${T.name}: ${name.value.trim()}`, `${T.town}: ${town.value}`);
    if (notes) lines.push(`${T.notes}: ${notes}`);
    status.textContent = T.opening;
    window.open(`https://wa.me/34621383059?text=${encodeURIComponent(lines.join('\n'))}`, '_blank', 'noopener');
  });

  renderPanel(); renderList();
  window.__proCleanCalc = { items, totals, add: () => root.querySelector('#add-item').click() };
})();
