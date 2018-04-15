GET /my_data/_search?pretty
{
  "query": {
        
        "match": {
          "Body" : "string"
        } 
  },
  "_source": ["Id", "Body"]
}



GET /my_data/_search?pretty
{
    "query": {
        "query_string": {
            "query": "importing csv into dict"
        }
    },
    "_source": [
        "Id",
        "Title",
        "Body"
    ],
    "highlight": {
        "fields": {
            "content": {}
        }
    }
}

GET /my_data/_search?pretty
{
    "query": {
        "bool": {
            "should": [
                {
                    "match": {
                        "Title": {
                            "query": "importing ",
                            "boost": 2
                        }
                    }
                },
                {
                    "match": {
                        "Body": {
                            "query": "importing csv into dict",
                            "boost": 1
                        }
                    }
                }
            ]
        }
    },
    "_source": [
        "Id",
        "Title",
        "Body"
    ],
    "highlight": {
        "fields": {
            "content": {}
        }
    }
}
