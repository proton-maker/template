module.exports = {
    content: ['./*.html'], // Path to HTML files
    css: ['./cim.css'], // Path to the combined CSS file
    output: './clean', // Output directory for the purified CSS
    defaultExtractor: content => content.match(/[\w-/:]+(?<!:)/g) || [],
  }
  