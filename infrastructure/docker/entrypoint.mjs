/**
 * Placeholder platform-app + worker process for template smoke tests.
 * Replace with the real platform-app image entrypoint in production.
 */
import http from 'node:http';

const role = process.env.ROLE ?? 'http';
const port = parseInt(process.env.PORT ?? '3000', 10);

if (role === 'worker') {
  console.log(`[deployment-template] worker heartbeat — replace with scheduler/worker entry (ROLE=${role})`);
  setInterval(() => {
    console.log('[deployment-template] worker tick');
  }, 60_000);
} else {
  const server = http.createServer((req, res) => {
    if (req.url === '/health') {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('ok');
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('deployment-template placeholder HTTP — see README');
  });
  server.listen(port, '0.0.0.0', () => {
    console.log(`[deployment-template] listening on ${port} (replace with platform-app)`);
  });
}
