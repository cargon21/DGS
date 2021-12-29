module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: {
      'dark-blue-color': '#150637',
      'pink-color': '#C424B3',
      'purple-color': '#450C85',
      'blue-color': '#2936C8',
      'light-blue-color': '#2797F4',
      'red-color' : '#821437',
      'black-color': '#000000',
      'faded-pink-color' : '#CD6D88',
      'off-white-color' : '#f8f8ff',
    },
    extend: {
      fontFamily: {
        prim: ['Grifter']
      }
      
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}


module.exports = {
  purge: {
    enabled: true,
    content: ['./Templates/*.html', './Templates/Admin/*.html', './Templates/Forms/*.html'],
 },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'dark-blue-color': '#150637',
        'pink-color': '#C424B3',
        'purple-color': '#450C85',
        'blue-color': '#2936C8',
        'light-blue-color': '#2797F4',
        'red-color' : '#821437',
        'black-color': '#000000',
        'faded-pink-color' : '#CD6D88',
        'off-white-color' : '#f8f8ff',
      },
      
      fontFamily: {
        prim: ['Grifter'],
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
