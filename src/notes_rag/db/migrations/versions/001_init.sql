CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chunks (
    id          BIGSERIAL PRIMARY KEY,
    source      TEXT NOT NULL,          -- relative path to the .md file
    chunk_index INTEGER NOT NULL,       -- position within the file
    content     TEXT NOT NULL,
    embedding   vector(384),            -- 384 for all-MiniLM-L6-v2
    strategy    TEXT NOT NULL,          -- 'recursive' | 'semantic'
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE (source, chunk_index, strategy)
);

CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);