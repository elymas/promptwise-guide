import type { APIRoute } from 'astro';
import coverage from '../../data/example-coverage.json';

export const GET: APIRoute = () => new Response(JSON.stringify(coverage, null, 2) + '\n', {
  headers: { 'Content-Type': 'application/json; charset=utf-8' },
});
