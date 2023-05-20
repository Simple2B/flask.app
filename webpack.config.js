//webpack.config.js
const path = require('path');

module.exports = {
  entry: {
    main: './src/main.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/main.js', // <--- Will be compiled to this single file
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
      },
    ],
  },
};
