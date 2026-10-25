'use strict';
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
for (const film of document.querySelectorAll('.film')) {
  const video = film.querySelector('video');
  const apply = () => { if (reduced.matches) { video.pause(); film.classList.add('reduced'); } else film.classList.remove('reduced'); };
  apply(); reduced.addEventListener('change', apply);
  film.querySelector('.motion-override')?.addEventListener('click', () => {film.classList.remove('reduced');video.focus();});
}
const explorer = document.querySelector('[data-trajectory]');
if (explorer) {
  const source = JSON.parse(document.querySelector('#trajectory-data').textContent);
  const slider = explorer.querySelector('input');
  const marker = explorer.querySelector('#host-marker');
  const output = explorer.querySelector('output');
  const draw = () => {
    const p = source.samples[Number(slider.value)];
    marker.setAttribute('cx', p.px); marker.setAttribute('cy', p.py);
    output.textContent = `t = ${p.t_s.toFixed(1)} s · inertial X = ${(p.x_m/1000).toFixed(3)} km · Z = ${(p.z_m/1000).toFixed(3)} km · host mass = ${p.mass_kg.toFixed(6)} kg`;
  };
  slider.addEventListener('input', draw);draw();
}
