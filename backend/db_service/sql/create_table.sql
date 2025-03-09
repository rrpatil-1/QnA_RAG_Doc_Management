CREATE TABLE {{table_name}} (
    id bigserial PRIMARY KEY, 
    content text, 
    embedding vector({{embedding_size}}), 
    source text
);