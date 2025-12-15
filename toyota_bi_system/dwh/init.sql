-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create schema for Toyota data
CREATE SCHEMA IF NOT EXISTS toyota_dw;

-- Set search path
SET search_path TO toyota_dw, public;