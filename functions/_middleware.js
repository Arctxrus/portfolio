/* ==========================================================================
   Cloudflare Pages Function middleware (rebrand + migration round, 2026-08-07).

   Deployment configuration, NOT runtime site code: this file never ships to the
   browser and is not referenced by index.html. It is Cloudflare Pages plumbing
   that runs on the edge BEFORE static assets are served, so it can force a 404 on
   the repo paths that are not part of the public site (build docs, history and
   tooling, which carry the owner's name and the full change log).

   Why this and not _redirects: in practice Cloudflare Pages serves a matching
   static asset BEFORE consulting _redirects, so the _redirects force-404 rules
   were ignored and /PROGRESS.md, /CONCEPT.md, /docs/*, /tools/*, /references/*
   and /verify/* all served real content at 200. A Pages Function middleware runs
   ahead of the static asset handler, so it is the reliable gate. _redirects is
   kept in place as harmless belt and braces.

   No build step is introduced: Cloudflare compiles functions/ at deploy time on
   its own platform; there is no local bundler, package.json or npm runtime
   dependency added to the repo. UK English, no em dashes.
   ========================================================================== */

const BLOCK_EXACT = ['/progress.md', '/concept.md', '/readme.md'];
const BLOCK_PREFIX = [
  '/verify/', '/docs/', '/tools/', '/references/', '/.claude/', '/functions/'
];

export async function onRequest(context) {
  const path = new URL(context.request.url).pathname.toLowerCase();
  const blocked =
    BLOCK_EXACT.indexOf(path) !== -1 ||
    BLOCK_PREFIX.some(function (prefix) { return path.indexOf(prefix) === 0; });

  if (blocked) {
    return new Response('Not found', {
      status: 404,
      headers: { 'content-type': 'text/plain; charset=utf-8' }
    });
  }

  return context.next();
}
