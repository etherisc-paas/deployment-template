-- Creates the six framework logical schemas on first database init (see product-framework migrations).
CREATE SCHEMA IF NOT EXISTS framework;
CREATE SCHEMA IF NOT EXISTS events;
CREATE SCHEMA IF NOT EXISTS assets;
CREATE SCHEMA IF NOT EXISTS ledger;
CREATE SCHEMA IF NOT EXISTS scheduler;
CREATE SCHEMA IF NOT EXISTS audit;
