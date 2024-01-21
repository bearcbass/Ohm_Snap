import type { Config } from "tailwindcss";
const defaultTheme = require("tailwindcss/defaultTheme")

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      fontFamily: {
				sans: ["var(--font-inter)", ...defaultTheme.fontFamily.sans],
				display: ["var(--font-calsans)"],
			},
      animation: {
        "fade-in": "fade-in 2s ease-in-out forwards"
      },
      keyframes: {
        "fade-in": {
          "0%": {
            opacity: "0%"
          },
          "70%": {
            opacity: "0%"
          },
          "100%": {
            opacity: "100%"
          }
        }
      }
    },
  },
  plugins: [
    require("@tailwindcss/typography"),
    // require("@tailwindscss/nesting"),
    require("tailwindcss-debug-screens")
    // require('postcss-preset-env')
  ],
};
export default config;
