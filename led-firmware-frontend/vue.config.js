
module.exports = {
  devServer: {
    port: 8181,
  },
  pages: {
    app: {
      entry: 'src/main.ts',
      template: 'public/index.html',
      filename: 'index.html',
    },
  },
  pluginOptions: {
    i18n: {
      locale: 'de',
      fallbackLocale: 'de',
      localeDir: 'locales',
      enableInSFC: true,
    },
  },
  configureWebpack: {
    devtool: 'source-map',
  },
  transpileDependencies: ['vuex-module-decorators']
};