import os
from flask import Flask
from flask.ext.assets import Environment, Bundle

def init(app):
  assets = Environment(app)
  if app.config.get('CARAVELA_ENV') == 'production':
    assets.debug=False
    assets.auto_build=False
  #else:
  #  assets.debug = True

  assets.url = app.static_url_path

  assets.register('common.js', Bundle(
    'lib/jquery-1.9.1.min.js',
    'lib/bootstrap.js',
    'lib/modernizr-2.6.1.min.js',
    'lib/underscore-min.js',
    'lib/less-1.3.0.min.js',

    'lib/jquery-ui-1.10.1.custom.min.js',
    'lib/jquery.mousewheel.js',

    'lib/handlebars-1.0.0.js',
    'lib/ember-1.0.0.js',
    'lib/ember-data.js',
    'lib/ember-table.js',


    'lib/d3.v3.min.js',
    'lib/vega.js',
    'lib/d3.geo.projection.min.js',


    'lib/codemirror.js',

    'lib/mode/javascript/javascript.js',


    'js/app.js',
    'js/routes/*.js',
    'js/controllers/*.js',
    'js/models/*.js',
    'js/views/*.js',
    
    #filters='rjsmin',
    output='assets/common.js'
  ))

  sass = Bundle(
    '**/*.sass',
    filters='compass', 
    output='assets/sass.css'
  )

  assets.register('sass.css', sass)

  assets.register('common.css', Bundle(
    sass,
    'css/bootstrap.min.css',
    'lib/codemirror.css',
    'css/persona-buttons.css',
    'css/style.css',

    output='assets/common.css'
  ))

  assets.config.update(dict(
    jst_compiler = "Em.Handlebars.compile",
    jst_namespace= "Em.TEMPLATES"
  ))

  assets.register('app.handlebars', Bundle(
    'templates/*.handlebars',
    'templates/**/*.handlebars',
    filters='jst',

    output='assets/app.handlebars'
  ))
  
