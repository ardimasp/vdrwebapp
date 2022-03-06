// const {defaults} = require('jest-config');
// module.exports = {
//   moduleFileExtensions: [...defaults.moduleFileExtensions, 'ts', 'tsx'],
//   transform: {
//       './vue$': 'index.js'
//   }
// };

const config = {
    verbose: true,
    testURL: 'http:/localhost/'
  };
  
  module.exports = config;

  module.exports = async () => {
    return {
        verbose: true,
        moduleFileExtensions: [
            "js",
            "json",
            "vue"
        ],
        transform: {
            ".*\\.(vue)$": "vue-jest",
            ".*\\.(js)$": "babel-jest"
        },
        testEnvironment: 'jsdom',
        setupFilesAfterEnv: [
            './tests/setup.js'
        ]
        // transformIgnorePatterns: ['/node_modules/']
    };
  };