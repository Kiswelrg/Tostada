import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

function externalizeIpa() {
  return {
    name: 'externalize-ipa', // A name for the plugin
    resolveId(source) {
      if (source.startsWith('/ipa/')) {
        return { id: source, external: true };
      }
      return null;
    }
  };
}

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {...process.env, ...loadEnv(mode, process.cwd())};
  const dev = mode === 'development';
  return defineConfig({
    plugins: [
      vue(),
      externalizeIpa()
    ],
    resolve: {
      alias: {
        "@": resolve(__dirname, './src'),
      },
    },
    build: {
      assetsDir: "static",
      outDir: resolve(__dirname, 'dist'),
      rollupOptions: {
        // input: {
        //   main: resolve(__dirname, 'index.html'),
        //   // signup: resolve(__dirname, 'user/index.html'),
        // },
        external: [
          /^ipa\/.*/,
        ]
      },
    },
    server: {
      proxy: {
        "/api": {
          target: process.env.VITE_BACKEND_URL,
          changeOrigin: dev,
          rewrite: (path) => path.replace(/^\/api/,'/'),
        },
        "/ipa": {
          target: dev ? process.env.VITE_FRONTEND_URL : process.env.VITE_BACKEND_URL,
          changeOrigin: dev,
          rewrite: (path) => {
            if (dev)
              return path.replace(/^\/ipa/,'/')
            else
              return path.replace(/^\/ipa/,'/static')
          },
        },
        
      }
    }
  });
}

