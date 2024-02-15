module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  parser: '@babel/eslint-parser', // Use the appropriate parser for your project
  parserOptions: {
    ecmaVersion: 2021, // Or the version you are targeting
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended', // Add the react-hooks/recommended configuration
  ],
  plugins: ['react', 'react-hooks'],
  rules: {
    // Add any additional ESLint rules or overrides here
  },
  settings: {
    react: {
      version: 'detect', // Automatically detect the React version
    },
  },
};
