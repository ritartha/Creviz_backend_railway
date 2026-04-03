/* ============================================================
   API CLIENT
   Talks to the Django REST backend at localhost:8000
============================================================ */
const API_BASE = 'http://10.1.63.21:8000/api';

const Api = (() => {

  // ── Token management ────────────────────────────────────────
  function getToken()         { return localStorage.getItem('access_token'); }
  function getRefresh()       { return localStorage.getItem('refresh_token'); }
  function setTokens(a, r)    { localStorage.setItem('access_token', a);
                                 localStorage.setItem('refresh_token', r); }
  function clearTokens()      { localStorage.removeItem('access_token');
                                 localStorage.removeItem('refresh_token');
                                 localStorage.removeItem('creviz_user'); }
  function isLoggedIn()       { return !!getToken(); }

  // ── Core request ─────────────────────────────────────────────
  async function request(method, path, data = null, auth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth && getToken()) {
      headers['Authorization'] = `Bearer ${getToken()}`;
    }

    const opts = { method, headers };
    if (data) opts.body = JSON.stringify(data);

    try {
      const res  = await fetch(API_BASE + path, opts);
      const text = await res.text();
      const json = text ? JSON.parse(text) : {};

      // Auto refresh token if 401
      if (res.status === 401 && auth && getRefresh()) {
        const refreshed = await refreshToken();
        if (refreshed) return request(method, path, data, auth);
        clearTokens();
        window.location.href = 'signin.html';
        return null;
      }

      return { ok: res.ok, status: res.status, data: json };
    } catch (err) {
      console.error('API error:', err);
      return { ok: false, status: 0, data: { detail: err.message } };
    }
  }

  async function refreshToken() {
    const refresh = getRefresh();
    if (!refresh) return false;
    const res = await fetch(API_BASE + '/auth/refresh/', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ refresh }),
    });
    if (res.ok) {
      const data = await res.json();
      localStorage.setItem('access_token', data.access);
      return true;
    }
    return false;
  }

  // ── Auth endpoints ────────────────────────────────────────────
  async function login(email, password) {
    const res = await request('POST', '/accounts/login/',
      { email, password }, false);
    if (res.ok) {
      setTokens(res.data.access, res.data.refresh);
      localStorage.setItem('creviz_user', JSON.stringify(res.data.user));
    }
    return res;
  }

  async function register(email, username, password, password2) {
    return request('POST', '/accounts/register/',
      { email, username, password, password2 }, false);
  }

  async function logout() {
    const refresh = getRefresh();
    if (refresh) {
      await request('POST', '/accounts/logout/', { refresh });
    }
    clearTokens();
  }

  function getUser() {
    const u = localStorage.getItem('creviz_user');
    return u ? JSON.parse(u) : null;
  }

  // ── Portfolio endpoints ───────────────────────────────────────
  async function getProjects(params = {}) {
    const qs = new URLSearchParams({ visible: 'true', ...params }).toString();
    return request('GET', `/portfolio/projects/?${qs}`);
  }

  // ── Marketplace endpoints ─────────────────────────────────────
  async function getProducts(params = {}) {
    const qs = new URLSearchParams(params).toString();
    return request('GET', `/marketplace/products/?${qs}`);
  }

  async function getFeatured() {
    return request('GET', '/marketplace/products/featured/');
  }

  async function getProduct(id) {
    return request('GET', `/marketplace/products/${id}/`);
  }

  // ── Order endpoint ────────────────────────────────────────────
  async function placeOrder(productId, fullName, email, notes = '') {
    return request('POST', '/marketplace/orders/', {
      product:   productId,
      full_name: fullName,
      email,
      notes,
    });
  }

  // ── Contact endpoint ──────────────────────────────────────────
  async function sendContact(fullName, email, subject, message) {
    return request('POST', '/contact/',
      { full_name: fullName, email, subject, message }, false);
  }

  // ── Commission endpoint ───────────────────────────────────────
  async function submitCommission(data) {
    return request('POST', '/commissions/', data, false);
  }

  return {
    login, register, logout,
    getUser, isLoggedIn, clearTokens,
    getProjects,
    getProducts, getFeatured, getProduct,
    placeOrder,
    sendContact,
    submitCommission,
  };
})();