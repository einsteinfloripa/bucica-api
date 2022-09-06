/// <reference types="vitest" />

import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  test: {},
  resolve: {
    alias: {
      "@controllers": path.resolve(__dirname, "./src/controllers/index"),
      "@db": path.resolve(__dirname, "./src/db/index"),
      "@factories": path.resolve(__dirname, "./src/factories/index"),
      "@middlewares": path.resolve(__dirname, "./src/middlewares/index"),
      "@models": path.resolve(__dirname, "./src/models/index"),
      "@repositories": path.resolve(__dirname, "./src/repositories/index"),
      "@routers": path.resolve(__dirname, "./src/routers/index"),
      "@services": path.resolve(__dirname, "./src/services/index"),
      "@utils": path.resolve(__dirname, "./src/utils/index"),
      "@schemas": path.resolve(__dirname, "./src/models/schemas/index"),
      "@interfaces": path.resolve(__dirname, "./src/models/interfaces/index"),
    },
  },
});
