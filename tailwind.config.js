/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //project level e joto templates ache, sobgulor upor eta search calabe.means- eta globally kaj kore.

    "./**/templates/**/*.html"  // eta just app level er jonno search korbe
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

