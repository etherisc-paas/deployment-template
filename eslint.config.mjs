export default [
  { ignores: ['dist/', 'node_modules/', 'postgres/data'] },
  {
    files: ['src/**/*.js', 'scripts/**/*.mjs', 'infrastructure/docker/entrypoint.mjs'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        console: 'readonly',
        process: 'readonly',
      },
    },
    rules: {
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    },
  },
];
