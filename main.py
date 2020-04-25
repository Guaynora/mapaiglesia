from flask import Flask, jsonify, request, render_template,redirect, url_for
from elasticsearch import Elasticsearch
from elasticsearch import helpers
#from flask_cors import CORS 
import json

app = Flask(__name__)
#CORS(app)

client = Elasticsearch(Host = 'http://127.0.0.1', PORT=9200)
client = Elasticsearch()


def createIndex(client):
  if client.indices.exists(index="iglesias"):
    print("ya existe este indice")
  else:  
    client.indices.create(
        index = "iglesias",
        body ={
            "settings":{"number_of_shards":1},
            "mappings":{
                "properties": {
                    "iglesias": {
                        "properties": {
                        "nombre":  { "type": "text" },
                        "pastor": { "type": "text"  },
                        "provincia":{"type":"text"},
                        "location":{"type":"geo_point"}
                        }  
                    }
                }
            },
        }
    )

def indexing_documentes():
    doc2=[
        {
        "_index" : "iglesias",
        "_type" : "_doc",
        "_id" : "1",
        "_source" : {
          "nombre" : "Ipul 24 de Diciembre",
          "pastor" : "Juan Pablo Guzman",
          "provincia" : "Panama",
          "latitud" : "9.090700",
          "longitud": "-79.361271"
        }
      },
      {
        "_index" : "iglesias",
        "_type" : "_doc",
        "_id" : "2",
        "_source" : {
          "nombre" : "Ipul Mañanitas",
          "pastor" : "Ricardo Gallardo",
          "provincia" : "Panama",
          "latitud" : "9.083224",
          "longitud": "-79.406489"
        }
      },
      {
        "_index" : "iglesias",
        "_type" : "_doc",
        "_id" : "3",
        "_source" : {
          "nombre" : "Ipul Central",
          "pastor" : "Desconocido",
          "provincia" : "Panama",
          "latitud" : "9.015055",
          "longitud": "-79.485709"
        }
      },
      {
        "_index" : "iglesias",
        "_type" : "_doc",
        "_id" : "4",
        "_source" : {
          "nombre" : "Ipul Vacamonte",
          "pastor" : "Gerardo G",
          "provincia" : "Panama",
          "latitud" : "8.909378",
          "longitud": "-79.709208"
        }
      },
      {
        "_index" : "iglesias",
        "_type" : "_doc",
        "_id" : "5",
        "_source" : {
          "nombre" : "Ipul Juan Diaz",
          "pastor" : "Jose Antonio Carrascal",
          "provincia" : "Panama",
          "latitud" : "9.045985",
          "longitud": "-79.447671"
        }
      }
    ]
    helpers.bulk(client,doc2)



#redireccion hacia el html que se presentara con el mapa
@app.route('/')
def index():
    createIndex(client)
    indexing_documentes()
    #res = client.get(index = "iglesias",id=1)
    #print(res['_source'])
    
    client.indices.refresh(index="iglesias")
    res = client.search(index="iglesias", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    latitud=[]
    longitud = []
    names = []
    pastores = []
    provincias = []
    for hit in res['hits']['hits']:
        latitud.append("%(latitud)s" % hit["_source"])
        longitud.append("%(longitud)s" % hit["_source"])
        names.append("%(nombre)s" % hit["_source"])
        pastores.append("%(pastor)s" % hit["_source"])
        provincias.append("%(provincia)s" % hit["_source"])
        #print("%(nombre)s: %(location)s" % hit["_source"])
    print (latitud[1])
    print(longitud[1])
    return render_template('map.html',latitud = latitud, longitud = longitud, names = names,pastores = pastores, provincias = provincias)



if __name__ == "__main__":
  app.run(debug=True)
