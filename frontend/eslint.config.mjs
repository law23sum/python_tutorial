import {fixupConfigRules} from "@eslint/compat";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import path from "node:path";
import {fileURLToPath} from "node:url";
import eslint from "@eslint/js";
import {FlatCompat} from "@eslint/eslintrc";
import tseslint from 'typescript-eslint';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
});
export default tseslint.config(
  {
    ignores: ["**/dist/", "**/.eslintrc.cjs", "**/*.cjs"],
  },
  eslint.configs.recommended,
  tseslint.configs.recommended,
  ...fixupConfigRules(compat.extends(
    "plugin:react-hooks/recommended",
  )), {
    plugins: {
      "react-refresh": reactRefresh,
    },
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
    rules: {
      "react-refresh/only-export-components": ["warn", {
        allowConstantExport: true,
      }],
    },
  });
