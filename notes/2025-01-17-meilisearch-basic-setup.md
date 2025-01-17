# meilisearch

* indices are implicitly created (schema?)

Enable vector store:

```
curl \
  -X PATCH 'MEILISEARCH_URL/experimental-features/' \
  -H 'Content-Type: application/json'  \
  --data-binary '{
    "vectorStore": true
  }'
```

Here: http://localhost:7700

```shell
$ curl -X PATCH http://localhost:7700/experimental-features/ -H 'Content-Type: application/json' --data-binary '{"vectorStore": true}'

{
  "vectorStore": true,
  "metrics": false,
  "logsRoute": false,
  "editDocumentsByFunction": false,
  "containsFilter": false
}
```

Try to set ollama embedder. Document template:

> https://www.meilisearch.com/docs/learn/ai_powered_search/getting_started_with_ai_search?utm_campaign=release-v1-8&utm_source=blog#design-a-prompt-template

```
curl \
  -X PATCH 'localhost:7700/indexes/docsup/settings/embedders' \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "products-openai": {
      "source": "ollama",
      "url": "k9:11434",
      "model": "nomic-embed-text",
      "documentTemplate": "{{doc.text}}"
    }
  }'
```

Ok:

```
curl \
  -X PATCH 'localhost:7700/indexes/docsup/settings/embedders' \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "products-openai": {
      "source": "ollama",
      "url": "k9:11434",
      "model": "nomic-embed-text",
      "documentTemplate": "{{doc.text}}"
    }
  }'
```

