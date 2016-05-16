var grunt = require('grunt');
var webpack = require('webpack');
var ManifestPlugin = require('webpack-manifest-plugin');

module.exports = function(grunt) {

  grunt.initConfig({
    watch: {
      scripts : {
        files: ['client/**/*.js'],
        tasks: ['force:on','webpack']
      }
    },
    webpack : {
      entry: [
        "./client/entry.js"
      ],
      output: {
        path: __dirname + '/server/static/scripts',
        filename: 'main.js',
      },
      module: {
        loaders: [
          {
            test: /\.js$/,
            exclude: /node_modules/,
            loaders: ['react-hot', 'babel'],
          }
        ]
      },
      plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new ManifestPlugin(),
        new webpack.NoErrorsPlugin()
      ]
    }
  });


  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-exec');
  grunt.loadNpmTasks('grunt-force');

  grunt.loadNpmTasks('grunt-webpack');

  grunt.registerTask('default', ['watch']);
  grunt.registerTask('build_server', ['jshint']);
  grunt.registerTask('terminate_server', ['jshint']);
};
