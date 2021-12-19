module.exports = {
  purge: ['./public/**/*.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
        sans: ['Avenir', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
      },
    extend: {
      colors: {
        'primary': '#283252', // Primary accent color, currently blue
        'primary-dark' : '#050F2D', // Used for hovering over a button
        'positive': '#2B7D2B', // Green, used to communicate approval
        'positive-light' : '#ABE2AB', // Lighter version of positive, should be used in table & charts
        'negative' : '#BB0000', // Red, used to communicate rejection
        'negative-light' : '#FF8888', // Lighter version of negative, should be used in table & charts
        'gray' : '#DFDFDF', // Used in table header
        'gray-light' : '#F2F2F2', // Used for background in table rows & chosen loan application section
        'text' : '#333333', // Color for normal text & titles
        'background' : '#F6F1EB',

        // Colors for the color coding for low, medium and high
        'cc-low' : '#EBF5FF',
        'cc-medium' : '#B2EDFF',
        'cc-high' : '#40BBE1',
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
