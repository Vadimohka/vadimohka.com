document.documentElement.classList.add('js');

const mobileMenuQuery = window.matchMedia('(max-width: 1150px)');
const menuControls = document.querySelectorAll('.menu-toggle[aria-controls]');
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
  menuControls.forEach(button => {
    const links = document.getElementById(button.getAttribute('aria-controls'));
    if(!links) return;
    if(!mobileMenuQuery.matches){
      links.hidden = false;
      button.setAttribute('aria-expanded','false');
      button.closest('.nav').classList.remove('is-open');
    }else if(button.getAttribute('aria-expanded') !== 'true'){
      links.hidden = true;
    }
  });
};
menuControls.forEach(button => {
  const links = document.getElementById(button.getAttribute('aria-controls'));
  if(!links) return;
  button.addEventListener('click', () => {
    setMenuState(button, links, button.getAttribute('aria-expanded') !== 'true');
  });
  button.addEventListener('keydown', event => {
    if(event.key !== 'Enter' && event.key !== ' ') return;
    event.preventDefault();
    setMenuState(button, links, button.getAttribute('aria-expanded') !== 'true');
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
  },{threshold:.12});
  reveals.forEach(el=>io.observe(el));
}
const light = document.querySelector('.cursor-light');
if(light){
  window.addEventListener('pointermove', e => {
    light.style.left = e.clientX + 'px';
    light.style.top = e.clientY + 'px';
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
