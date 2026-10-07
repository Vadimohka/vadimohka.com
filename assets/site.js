document.documentElement.classList.add('js');

const mobileMenuQuery = window.matchMedia('(max-width: 1150px)');
const menuControls = document.querySelectorAll('.menu-toggle[aria-controls]');
// CSS can hide a focused control before the media-query callback runs.
let menuFocus = null;
document.addEventListener('focusin', event => {
  menuFocus = event.target.closest('.nav') ? event.target : null;
});
document.addEventListener('pointerdown', event => {
  if(!event.target.closest('.nav')) menuFocus = null;
});
window.addEventListener('blur', () => { menuFocus = null; });
const setMenuState = (button, links, open, returnFocus = false) => {
  const nav = button.closest('.nav');
  button.setAttribute('aria-expanded', String(open));
  links.hidden = !open;
  nav.classList.toggle('is-open', open);
  if(open){
    const firstLink = links.querySelector('a');
    if(firstLink) firstLink.focus();
  }else if(returnFocus){
    button.focus();
  }
};
const syncMenusToViewport = () => {
  const active = document.activeElement === document.body ? menuFocus : document.activeElement;
  menuControls.forEach(button => {
    const links = document.getElementById(button.getAttribute('aria-controls'));
    if(!links) return;
    if(!mobileMenuQuery.matches){
      links.hidden = false;
      if(active === button) links.querySelector('a')?.focus();
      button.setAttribute('aria-expanded','false');
      button.closest('.nav').classList.remove('is-open');
    }else if(button.getAttribute('aria-expanded') !== 'true'){
      const focusInMenu = links.contains(active);
      links.hidden = true;
      if(focusInMenu) button.focus();
    }
  });
};
menuControls.forEach(button => {
  const links = document.getElementById(button.getAttribute('aria-controls'));
  if(!links) return;
  button.addEventListener('click', () => {
    setMenuState(button, links, button.getAttribute('aria-expanded') !== 'true');
  });
  // Keep the whole focused link visible in a height-limited landscape menu.
  // Some engines focus a partially clipped link without scrolling its container.
  links.addEventListener('focusin', () => {
    requestAnimationFrame(() => {
      const active = document.activeElement;
      if(!mobileMenuQuery.matches || links.hidden || !links.contains(active)) return;
      const link = active.getBoundingClientRect();
      const menu = links.getBoundingClientRect();
      const top = menu.top + links.clientTop + 6;
      const bottom = menu.top + links.clientTop + links.clientHeight - 6;
      if(link.top < top) links.scrollTop += link.top - top;
      else if(link.bottom > bottom) links.scrollTop += link.bottom - bottom;
    });
  });
  // Native button activation already handles Enter and Space.
  button.closest('.nav').addEventListener('focusout', () => {
    requestAnimationFrame(() => {
      if(mobileMenuQuery.matches && !button.closest('.nav').contains(document.activeElement)){
        setMenuState(button, links, false);
      }
    });
  });
  links.addEventListener('click', event => {
    if(event.target.closest('a') && mobileMenuQuery.matches) setMenuState(button, links, false);
  });
});
document.addEventListener('keydown', event => {
  if(event.key !== 'Escape') return;
  menuControls.forEach(button => {
    const links = document.getElementById(button.getAttribute('aria-controls'));
    if(links && button.getAttribute('aria-expanded') === 'true') setMenuState(button, links, false, true);
  });
});
document.addEventListener('click', event => {
  menuControls.forEach(button => {
    const nav = button.closest('.nav');
    const links = document.getElementById(button.getAttribute('aria-controls'));
    if(links && button.getAttribute('aria-expanded') === 'true' && !nav.contains(event.target)) setMenuState(button, links, false);
  });
});
if(typeof mobileMenuQuery.addEventListener === 'function') mobileMenuQuery.addEventListener('change', syncMenusToViewport);
syncMenusToViewport();

// Keep anchor offsets and the landscape menu tied to the actual header height.
const siteHeader = document.querySelector('.site-header');
const syncHeaderHeight = () => {
  if(siteHeader) document.documentElement.style.setProperty('--header-height', `${siteHeader.getBoundingClientRect().height}px`);
};
syncHeaderHeight();
if(siteHeader && 'ResizeObserver' in window) new ResizeObserver(syncHeaderHeight).observe(siteHeader);
else window.addEventListener('resize', syncHeaderHeight, {passive:true});

const skipLink = document.querySelector('.skip-link');
const mainContent = document.getElementById('main-content');
if(skipLink && mainContent){
  skipLink.addEventListener('click', event => {
    event.preventDefault();
    mainContent.focus({preventScroll:true});
    mainContent.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',block:'start'});
  });
}

const reveals = document.querySelectorAll('.reveal');
if(!('IntersectionObserver' in window)){
  reveals.forEach(el=>el.classList.add('is-visible'));
}else{
  const io = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=>{ if(entry.isIntersecting){ entry.target.classList.add('is-visible'); io.unobserve(entry.target);} });
  },{threshold:0});
  reveals.forEach(el=>io.observe(el));
}
const light = document.querySelector('.cursor-light');
if(light){
  const pointerEffects = window.matchMedia('(hover:hover) and (pointer:fine) and (prefers-reduced-motion:no-preference)');
  window.addEventListener('pointermove', e => {
    if(!pointerEffects.matches) return;
    light.style.setProperty('--pointer-x', e.clientX + 'px');
    light.style.setProperty('--pointer-y', e.clientY + 'px');
  }, {passive:true});
}
const intentCards = document.querySelectorAll('.intent-card[data-intent]');
const routeResponse = document.querySelector('[data-route-response]');
const routeTitle = routeResponse?.querySelector('[data-route-title]');
const routeCopy = routeResponse?.querySelector('[data-route-copy]');
const routeDetails = {
  enterprise: {title:'Enterprise AI deployment', copy:'Share the use case, the operating boundary and the decision you need to make next.'},
  diligence: {title:'AI product assessment', copy:'Share the product stage, the question behind the decision and the areas that need a closer look.'},
  founder: {title:'CTO diagnostic', copy:'Share where product, architecture, ownership or delivery have stopped lining up.'},
  executive: {title:'Executive AI briefing', copy:'Share the audience, the decision and the context that needs to become clear.'},
  media: {title:'Expert comment', copy:'Share the publication, deadline, audience and question you want addressed.'},
  speaking: {title:'Speaking invitation', copy:'Share the audience, format, language, date and topic.'}
};
const setIntent = (intent, {updateUrl = false, focus = false} = {}) => {
  const details = routeDetails[intent];
  if(!details) return;
  intentCards.forEach(card => {
    const selected = card.dataset.intent === intent;
    card.classList.toggle('is-selected', selected);
    if(selected) card.setAttribute('aria-current','true');
    else card.removeAttribute('aria-current');
  });
  if(routeResponse){
    routeResponse.dataset.activeRoute = intent;
    routeResponse.classList.add('is-active');
    if(routeTitle) routeTitle.textContent = details.title;
    if(routeCopy) routeCopy.textContent = details.copy;
    if(focus){
      routeResponse.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block:'nearest'});
      routeTitle?.focus({preventScroll:true});
    }
  }
  if(updateUrl){
    const url = new URL(window.location.href);
    url.searchParams.set('intent', intent);
    url.hash = 'contact';
    window.history.pushState({intent}, '', url);
  }
};
if(intentCards.length){
  const initialIntent = new URLSearchParams(window.location.search).get('intent');
  if(initialIntent) setIntent(initialIntent);
  intentCards.forEach(card => {
    const link = card.querySelector('a[href*="intent="]');
    if(!link) return;
    link.addEventListener('click', event => {
      const intent = card.dataset.intent;
      if(!routeDetails[intent] || !routeResponse) return;
      event.preventDefault();
      setIntent(intent, {updateUrl:true, focus:true});
    });
  });
  window.addEventListener('popstate', () => {
    const intent = new URLSearchParams(window.location.search).get('intent');
    if(intent) setIntent(intent);
  });
}
