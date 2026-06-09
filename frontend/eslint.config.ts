import pluginVue from 'eslint-plugin-vue'
import { defineConfigWithVueTs, vueTsConfigs } from '@vue/eslint-config-typescript'
import globals from 'globals'

export default defineConfigWithVueTs(
  {
    name: 'app/files-to-lint',
    files: ['**/*.{ts,mts,tsx,vue}'],
  },
  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/node_modules/**'],
  },
  {
    languageOptions: {
      globals: { ...globals.browser },
    },
  },
  pluginVue.configs['flat/essential'],
  vueTsConfigs.recommended,
  // Project overrides — MUST come last so they win over the shared configs above.
  {
    name: 'app/overrides',
    rules: {
      // Allow intentionally-unused args/vars prefixed with underscore.
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_' }],
      // Pre-existing `any` usage in the chart/survey views — surfaced as a warning
      // (tech debt to tighten incrementally) rather than blocking lint/CI.
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
)
