module.exports = {
  chainWebpack: config => {
    config.module
      .rule('fonts')
      .use('url-loader')
      .loader('file-loader')
      .tap(options => {
        options = {
          name: 'fonts/[name].[ext]'
        }
        return options
      })

    if (process.env.NODE_ENV === 'production') {
      config.plugin('html-webpack')
        .use(require('html-webpack-plugin'), [{
          filename: 'demo.html',
          template: 'src/index.wc.html',
        }])

      config.plugin('webpack-cdn')
        .use(require('webpack-cdn-plugin'), [{
          modules: [
            {name: '@webcomponents/webcomponentsjs', path: 'webcomponents-loader.js'},
            {name: 'vue', var: 'Vue', path: 'dist/vue.runtime.min.js'},
          ],
        }])
    }
  },
  devServer: {
    proxy: {
      '/song*': {
        target: 'http://localhost:5001',
        secure: false,
        changeOrigin: true
      },
      '/static*': {
        target: 'http://localhost:5001',
        secure: false,
        changeOrigin: true
      }
    }
  }
}
