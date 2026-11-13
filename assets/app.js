(() => {
  const doc = document.documentElement;
  doc.classList.add('js');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  /* Scroll reveal: once per element */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  /* Mobile menu */
  const btn = document.querySelector('.menu-btn');
  const menu = document.getElementById('mobile-menu');
  const setMenu = (open) => {
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    if (open) {
      menu.hidden = false;
      const items = [...menu.querySelectorAll('li')];
      const step = Math.min(60, 400 / items.length);
      items.forEach((li, i) => { li.style.transitionDelay = `${i * step}ms`; });
      requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('open')));
    } else {
      menu.classList.remove('open');
      menu.querySelectorAll('li').forEach((li) => { li.style.transitionDelay = '0ms'; });
      setTimeout(() => { if (!menu.classList.contains('open')) menu.hidden = true; }, 500);
    }
  };
  btn.addEventListener('click', () => setMenu(btn.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !menu.hidden) setMenu(false); });

  /* Current section in nav */
  const links = [...document.querySelectorAll('.nav-links a')];
  const sections = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const navIo = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => {
        const on = a.getAttribute('href') === `#${e.target.id}`;
        a.classList.toggle('active', on);
        if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  sections.forEach((s) => navIo.observe(s));

  /* Tagline: words light up one by one as they cross the trigger line */
  const tag = document.querySelector('[data-reveal-words]');
  if (tag) {
    const html = tag.innerHTML.split(/(<br\s*\/?>)/i).map((part) =>
      /^<br/i.test(part) ? part : part.split(/(\s+)/).map((w) => (w.trim() ? `<span class="w">${w}</span>` : w)).join('')
    ).join('');
    tag.innerHTML = html;
    const words = [...tag.querySelectorAll('.w')];
    if (reduced) {
      words.forEach((w) => w.classList.add('on'));
    } else {
      let ticking = false;
      const update = () => {
        ticking = false;
        const line = window.innerHeight * 0.7;
        const r = tag.getBoundingClientRect();
        // progress from when the block top hits the line until its bottom reaches 40% of viewport
        const start = line, end = window.innerHeight * 0.35;
        const p = Math.min(1, Math.max(0, (start - r.top) / (start - end + r.height * 0.6)));
        const n = Math.round(p * words.length);
        words.forEach((w, i) => w.classList.toggle('on', i < n));
      };
      const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      update();
    }
  }

  /* Quote form → WhatsApp */
  const form = document.getElementById('quote-form');
  if (form) {
    const status = document.getElementById('form-status');
    const itemsErr = document.getElementById('items-error');
    const qty = [...form.querySelectorAll('.item input')];
    qty.forEach((inp) => inp.addEventListener('input', () => {
      inp.closest('.item').classList.toggle('filled', Number(inp.value) > 0);
      if (qty.some((q) => Number(q.value) > 0)) itemsErr.hidden = true;
    }));
    const showErr = (el, show) => {
      el.classList.toggle('invalid', show);
      el.setAttribute('aria-invalid', String(show));
      const msg = el.closest('.field').querySelector('.field-error');
      if (msg) msg.hidden = !show;
    };
    ['name', 'town'].forEach((n) => form.elements[n].addEventListener('input', (e) => {
      if (e.target.value.trim()) showErr(e.target, false);
    }));
    form.elements.town.addEventListener('change', (e) => { if (e.target.value) showErr(e.target, false); });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const chosen = qty.filter((q) => Number(q.value) > 0);
      const name = form.elements.name;
      const town = form.elements.town;
      let ok = true;
      itemsErr.hidden = chosen.length > 0; if (!chosen.length) ok = false;
      showErr(name, !name.value.trim()); if (!name.value.trim()) ok = false;
      showErr(town, !town.value); if (!town.value) ok = false;
      if (!ok) {
        status.textContent = 'Some details are missing. Check the highlighted fields.';
        (form.querySelector('.invalid') || qty[0]).focus();
        return;
      }
      const lines = [
        `Hello Pro Clean, I would like a quote.`,
        ``,
        ...chosen.map((q) => `• ${q.name}: ${q.value}`),
        ``,
        `Name: ${name.value.trim()}`,
        `Town: ${town.value}`,
      ];
      const notes = form.elements.notes.value.trim();
      if (notes) lines.push(`Notes: ${notes}`);
      const url = `https://wa.me/34621383059?text=${encodeURIComponent(lines.join('\n'))}`;
      status.textContent = 'Opening WhatsApp with your request.';
      window.open(url, '_blank', 'noopener');
    });
  }
})();
