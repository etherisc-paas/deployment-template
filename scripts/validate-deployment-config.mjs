#!/usr/bin/env node
/**
 * Phase 1 stub — validates `products[]` exists. Phase 7 validates integration slots vs manifests.
 */
import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const primary = join(root, 'config/deployment-config.json');
const fallback = join(root, 'config/deployment-config.example.json');
const path = existsSync(primary) ? primary : fallback;
const raw = readFileSync(path, 'utf8');
const doc = JSON.parse(raw);
if (!Array.isArray(doc.products) || doc.products.length === 0) {
  console.error('deployment-config: missing products[]');
  process.exit(1);
}
console.warn('[validate-deployment-config] stub OK — Point to deployment-config.json in real forks');
process.exit(0);
