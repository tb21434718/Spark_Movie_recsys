import time, sys, cherrypy, os
from paste.translogger import TransLogger
from webapp import create_app
from pyspark import SparkContext, SparkConf
# path = "/home/dreamcity/Project/myproject/venv/lib/python2.7/site-packages"
# sys.path.append(path)
def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("movie_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
    # sc = SparkContext(conf=conf, pyFiles=['rec_engine.py', 'app.py'])
    sc = SparkContext(conf=conf)
 
    return sc
 
 
def run_server(app): 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
 
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '127.0.0.1'
    })
 
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
 
 
if __name__ == "__main__":
    # Init spark context and load libraries
    sc = init_spark_context()
    dataset_path = os.path.join('dataset','data_model')
    app = create_app(sc, dataset_path)
 
    # start web server
    run_server(app)

