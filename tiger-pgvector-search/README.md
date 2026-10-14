# Implement AI-Powered Vector Search with pgvector

`walk_notes` hypertable storing walk notes alongside `VECTOR(8)` embeddings, indexed with
**DiskANN** from pgvectorscale. Searches combine cosine similarity with time-range filters
in one SQL query, with no separate vector database.

- SQL: [vector_search.sql](vector_search.sql)
- Extensions: `vector` 0.8.7, `vectorscale` 0.9.0

## Results

| Query                                        | Top hit                                                  | Distance |
|----------------------------------------------|----------------------------------------------------------|---------:|
| "peaceful nature", all time                  | Quiet walk along the river, watched egrets               | 0.019    |
| "festival + food + people", last 10 days     | Pandal hopping with grandkids, ate jalebi at the mela    | 0.086    |
| "food with friends", older than 10 days      | Chai and samosa at the corner stall with old friends     | 0.020    |

## Note on embeddings

The embeddings are hand-assigned 8-dim theme scores (temple, market, nature, festival, food,
social, effort, weather), because the service has no `pgai` extension and no embedding API key
was used. The storage, index, and hybrid search are real; swapping in model-generated
embeddings (e.g. 1536-dim) only changes the column size and the insert step.
