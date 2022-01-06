// const IS_PRODUCTION = process.env.NODE_ENV === 'production'

const webpack = require('webpack');

module.exports = {
  outputDir: 'dist',
  assetsDir: 'static',
  lintOnSave: false,
  configureWebpack: {
    // Set up all the aliases we use in our app.
    resolve: {
      alias: {
        'chart.js': 'chart.js/dist/Chart.js'
      }
    },
    plugins: [
      new webpack.optimize.LimitChunkCountPlugin({
        maxChunks: 6
      })
    ]
  },
  pwa: {
    name: 'Vue Black Dashboard',
    themeColor: '#344675',
    msTileColor: '#344675',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: '#344675'
  },
  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false
    }
  },
  css: {
    // Enable CSS source maps.
    sourceMap: process.env.NODE_ENV !== 'production'
  }
};



// module.exports = {
//   outputDir: 'dist',
//   assetsDir: 'static',
//   // baseUrl: IS_PRODUCTION
//   // ? 'http://cdn123.com'
//   // : '/',
//   // For Production, replace set baseUrl to CDN
//   // And set the CDN origin to `yourdomain.com/static`
//   // Whitenoise will serve once to CDN which will then cache
//   // and distribute
//   // devServer: {
//   //   proxy: {
//   //     '/api*': {
//   //       // Forward frontend dev server request for /api to django dev server
//   //       target: 'http://localhost:8000/',
//   //     }
//   //   }
//   // }
// }
