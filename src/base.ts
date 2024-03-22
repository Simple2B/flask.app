import 'flowbite';
import { initDismisses } from 'flowbite';

export interface HTMXEventDetail {
  xhr: XMLHttpRequest;
  target: HTMLElement;
}

const themeToggleDarkIcons = document.querySelectorAll(
  '#theme-toggle-dark-icon',
);
const themeToggleLightIcons = document.querySelectorAll(
  '#theme-toggle-light-icon',
);

// Change the icons inside the button based on previous settings
if (
  localStorage.getItem('color-theme') === 'dark' ||
  (!('color-theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  themeToggleLightIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.add('dark');
} else {
  themeToggleDarkIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.remove('dark');
}

const themeToggleButtons = document.querySelectorAll('#theme-toggle');

themeToggleButtons.forEach(function (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', function () {
    // toggle icons inside button
    themeToggleDarkIcons.forEach(function (themeToggleDarkIcon) {
      themeToggleDarkIcon.classList.toggle('hidden');
    });

    themeToggleLightIcons.forEach(function (themeToggleLightIcon) {
      themeToggleLightIcon.classList.toggle('hidden');
    });

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
      if (localStorage.getItem('color-theme') === 'light') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
      }

      // if NOT set via local storage previously
    } else {
      if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
      } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
      }
    }
  });
});

const backgroundModalElement = document.getElementById('custom-modal-content').parentElement;
backgroundModalElement.addEventListener('click', () => {
  if (!backgroundModalElement.classList.contains('hidden')) {
    backgroundModalElement.classList.add('hidden')
  }
})

document.addEventListener('htmx:afterSwap', (e:  CustomEvent<HTMXEventDetail>) => {
  if ([404, 202].includes(e.detail.xhr.status)) {
    initDismisses();
    return
  } 
  if (backgroundModalElement.classList.contains('hidden')) {
    backgroundModalElement.classList.remove('hidden')
  }

});