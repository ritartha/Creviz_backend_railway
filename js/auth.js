/* ============================================================
   AUTH — handles sign-in, sign-up forms and nav state
============================================================ */
document.addEventListener('DOMContentLoaded', () => {

  // ── Update navbar based on login state ──────────────────────
  updateNavAuth();

  // ── Sign In form ─────────────────────────────────────────────
  const signinForm = document.getElementById('signinForm');
  if (signinForm) {
    signinForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      clearErrors();

      const email    = document.getElementById('siEmail').value.trim();
      const password = document.getElementById('siPass').value;
      const btn      = document.getElementById('signinBtn');
      const feedback = document.getElementById('signinFeedback');

      if (!email) {
        showFieldError('siEmailErr', 'Email is required.');
        return;
      }
      if (!password) {
        showFieldError('siPassErr', 'Password is required.');
        return;
      }

      setLoading(btn, true);
      const res = await Api.login(email, password);
      setLoading(btn, false);

      if (res.ok) {
        showFeedback(feedback, 'success', 'Login successful! Redirecting...');
        setTimeout(() => {
          window.location.href =
            new URLSearchParams(window.location.search).get('next') ||
            'index.html';
        }, 800);
      } else {
        const msg = res.data.detail || 'Invalid email or password.';
        showFeedback(feedback, 'error', msg);
      }
    });
  }

  // ── Sign Up form ──────────────────────────────────────────────
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    // Password strength checker
    const passInput    = document.getElementById('suPass');
    const strengthFill = document.getElementById('strengthFill');
    const strengthLbl  = document.getElementById('strengthLabel');

    if (passInput && strengthFill) {
      passInput.addEventListener('input', () => {
        const val    = passInput.value;
        const score  = getPasswordScore(val);
        const levels = [
          { w: '20%',  bg: '#ef4444', label: 'Weak',      color: '#ef4444' },
          { w: '40%',  bg: '#f97316', label: 'Fair',      color: '#f97316' },
          { w: '60%',  bg: '#fbbf24', label: 'Good',      color: '#fbbf24' },
          { w: '80%',  bg: '#4ade80', label: 'Strong',    color: '#4ade80' },
          { w: '100%', bg: '#4ade80', label: 'Very Strong', color: '#4ade80' },
        ];
        const lvl = levels[Math.min(score, 4)];
        strengthFill.style.width      = val.length ? lvl.w  : '0';
        strengthFill.style.background = lvl.bg;
        strengthLbl.textContent       = val.length ? lvl.label : '';
        strengthLbl.style.color       = lvl.color;
      });
    }

    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      clearErrors();

      const username  = document.getElementById('suUsername').value.trim();
      const email     = document.getElementById('suEmail').value.trim();
      const password  = document.getElementById('suPass').value;
      const password2 = document.getElementById('suPass2').value;
      const agree     = document.getElementById('agreeTerms').checked;
      const btn       = document.getElementById('signupBtn');
      const feedback  = document.getElementById('signupFeedback');

      let valid = true;

      if (!username) {
        showFieldError('suUsernameErr', 'Username is required.'); valid = false;
      }
      if (!email) {
        showFieldError('suEmailErr', 'Email is required.'); valid = false;
      }
      if (password.length < 8) {
        showFieldError('suPassErr', 'Password must be at least 8 characters.'); valid = false;
      }
      if (password !== password2) {
        showFieldError('suPass2Err', 'Passwords do not match.'); valid = false;
      }
      if (!agree) {
        showFeedback(feedback, 'error', 'You must agree to the Terms of Service.');
        return;
      }
      if (!valid) return;

      setLoading(btn, true);
      const res = await Api.register(email, username, password, password2);
      setLoading(btn, false);

      if (res.ok) {
        showFeedback(feedback, 'success',
          'Account created! Signing you in...');
        const loginRes = await Api.login(email, password);
        if (loginRes.ok) {
          setTimeout(() => { window.location.href = 'index.html'; }, 1000);
        } else {
          setTimeout(() => { window.location.href = 'signin.html'; }, 1000);
        }
      } else {
        const errors = res.data;
        let msg = '';
        if (errors.email)    msg += errors.email.join(' ') + ' ';
        if (errors.username) msg += errors.username.join(' ') + ' ';
        if (errors.password) msg += errors.password.join(' ') + ' ';
        if (errors.detail)   msg += errors.detail;
        showFeedback(feedback, 'error', msg || 'Registration failed.');
      }
    });
  }

  // ── Password visibility toggle ────────────────────────────────
  document.querySelectorAll('.toggle-pass').forEach(btn => {
    btn.addEventListener('click', () => {
      const input = btn.closest('.input-wrap').querySelector('input');
      const icon  = btn.querySelector('i');
      if (input.type === 'password') {
        input.type     = 'text';
        icon.className = 'fa-solid fa-eye-slash';
      } else {
        input.type     = 'password';
        icon.className = 'fa-solid fa-eye';
      }
    });
  });

  // ── Contact form ──────────────────────────────────────────────
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const feedback = document.getElementById('contactFeedback');
      const btn      = document.getElementById('contactSubmit');
      const data     = Object.fromEntries(new FormData(contactForm));

      setLoading(btn, true);
      const res = await Api.sendContact(
        data.full_name, data.email, data.subject, data.message);
      setLoading(btn, false);

      if (res.ok) {
        showFeedback(feedback, 'success',
          'Message sent! I will get back to you soon.');
        contactForm.reset();
      } else {
        showFeedback(feedback, 'error',
          'Something went wrong. Please try again.');
      }
    });
  }
});

// ── Helpers ───────────────────────────────────────────────────
function updateNavAuth() {
  const user     = Api.getUser();
  const actions  = document.querySelector('.nav-actions');
  if (!actions) return;

  if (user && Api.isLoggedIn()) {
    const signinBtn  = actions.querySelector('a[href="signin.html"]');
    const signupBtn  = actions.querySelector('a[href="signup.html"]');
    if (signinBtn) signinBtn.remove();
    if (signupBtn) {
      signupBtn.textContent = user.username || user.email;
      signupBtn.href        = '#';
      signupBtn.className   = 'btn btn-outline btn-sm';
      const logoutBtn       = document.createElement('a');
      logoutBtn.href        = '#';
      logoutBtn.className   = 'btn btn-ghost btn-sm';
      logoutBtn.textContent = 'Logout';
      logoutBtn.addEventListener('click', async (e) => {
        e.preventDefault();
        await Api.logout();
        window.location.reload();
      });
      actions.insertBefore(logoutBtn, actions.querySelector('.nav-toggle'));
    }
  }
}

function showFieldError(id, msg) {
  const el = document.getElementById(id);
  if (el) el.textContent = msg;
}

function clearErrors() {
  document.querySelectorAll('.field-error').forEach(el => {
    el.textContent = '';
  });
  document.querySelectorAll('.form-feedback').forEach(el => {
    el.className   = 'form-feedback';
    el.textContent = '';
  });
}

function showFeedback(el, type, msg) {
  if (!el) return;
  el.className   = `form-feedback ${type}`;
  el.textContent = msg;
}

function setLoading(btn, loading) {
  if (!btn) return;
  if (loading) {
    btn.dataset.originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Please wait...';
    btn.disabled  = true;
  } else {
    btn.innerHTML = btn.dataset.originalText || btn.innerHTML;
    btn.disabled  = false;
  }
}

function getPasswordScore(password) {
  let score = 0;
  if (password.length >= 8)  score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password))         score++;
  if (/[0-9]/.test(password))         score++;
  if (/[^A-Za-z0-9]/.test(password))  score++;
  return Math.min(score, 4);
}

function showToast(msg, type = 'info', duration = 3500) {
  const icons = {
    success: 'fa-circle-check',
    error:   'fa-circle-xmark',
    info:    'fa-circle-info',
  };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <i class="fa-solid ${icons[type] || icons.info} toast-icon-${type}"></i>
    <span>${msg}</span>
  `;
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity   = '0';
    toast.style.transform = 'translateY(12px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}