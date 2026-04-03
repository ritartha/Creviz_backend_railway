/* ============================================================
   PORTFOLIO — loads projects from Django API and renders cards
============================================================ */
document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('portfolioGrid');
  if (!grid) return;

  // Show skeleton loaders
  grid.innerHTML = Array(6).fill(0).map(() => `
    <article class="project-card">
      <div class="skeleton" style="height:220px;border-radius:0;"></div>
      <div class="card-body">
        <div class="skeleton" style="height:16px;width:80px;margin-bottom:10px;"></div>
        <div class="skeleton" style="height:22px;width:60%;margin-bottom:8px;"></div>
        <div class="skeleton" style="height:60px;margin-bottom:12px;"></div>
        <div class="skeleton" style="height:14px;width:40%;"></div>
      </div>
    </article>
  `).join('');

  // Fetch from API
  let projects = [];
  try {
    const res = await Api.getProjects({ page_size: 100 });
    if (res && res.ok) {
      projects = res.data.results || res.data;
    }
  } catch (e) {
    console.warn('API unavailable — loading fallback data.');
  }

  // Render
  renderProjects(projects, 'all');

  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      filterAndRender(projects, btn.dataset.filter);
    });
  });
});

function filterAndRender(projects, filter) {
  const filtered = filter === 'all'
    ? projects
    : projects.filter(p => p.category === filter);
  renderProjects(filtered, filter);
}

function renderProjects(projects, filter) {
  const grid = document.getElementById('portfolioGrid');
  if (!grid) return;

  if (!projects || projects.length === 0) {
    grid.innerHTML = `
      <div style="grid-column:1/-1;text-align:center;
                  padding:60px;color:var(--text-400);">
        <i class="fa-solid fa-cube"
           style="font-size:3rem;margin-bottom:16px;opacity:0.3;
                  display:block;"></i>
        <p>No projects found.</p>
      </div>`;
    return;
  }

  grid.innerHTML = projects.map(p => {
    const category    = p.category || 'environment';
    const title       = p.title || '';
    const desc        = p.description || p.desc || '';
    const icon        = p.icon || 'fa-solid fa-cube';
    const gradient    = p.gradient || 'env-gradient';
    const tools       = p.tools || [];
    const image       = p.image