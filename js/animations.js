/* ============================================================
   ANIMATIONS — intersection observer scroll reveals
   + counter animation + skill bar animation
============================================================ */
document.addEventListener('DOMContentLoaded', () => {

  // ── Scroll reveal ──────────────────────────────────────────
  const revealEls = document.querySelectorAll(
    '.reveal-up, .reveal-left, .reveal-right');

  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => revealObs.observe(el));

  // ── Counter animation ──────────────────────────────────────
  const counters = document.querySelectorAll('[data-target]');
  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el     = entry.target;
      const target = parseInt(el.dataset.target, 10);
      const dur    = 1800;
      const step   = 16;
      const inc    = target / (dur / step);
      let   current = 0;

      const timer = setInterval(() => {
        current += inc;
        if (current >= target) {
          el.textContent = target;
          clearInterval(timer);
        } else {
          el.textContent = Math.floor(current);
        }
      }, step);

      counterObs.unobserve(el);
    });
  }, { threshold: 0.5 });

  counters.forEach(el => counterObs.observe(el));

  // ── Skill bars ─────────────────────────────────────────────
  const skillFills = document.querySelectorAll('.skill-fill');
  const skillObs   = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el    = entry.target;
      const width = el.dataset.width || '0';
      setTimeout(() => { el.style.width = width + '%'; }, 100);
      skillObs.unobserve(el);
    });
  }, { threshold: 0.5 });

  skillFills.forEach(el => skillObs.observe(el));
});