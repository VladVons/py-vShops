/*
Created: 2023.11.13
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/

function goToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.onscroll = function() {
  var scrollPosition = document.documentElement.scrollTop || document.body.scrollTop;
  var goTopBtn = document.getElementById('vBtn-GoTop');

  if (scrollPosition > 100) {
    goTopBtn.style.display = 'block';
  } else {
    goTopBtn.style.display = 'none';
  }
};
