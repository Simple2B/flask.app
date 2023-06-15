const {merge} = require('webpack-merge');
const common = require('./webpack.config.js');

module.exports = common.map(conf =>
  merge(conf, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
      static: './app/static/js',
    },
  }),
);
