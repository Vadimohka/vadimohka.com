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
