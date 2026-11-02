import assert from 'node:assert/strict';
import test from 'node:test';
import { apply } from '../.agents/skills/vercel-optimize/lib/sanitizers/vercel-directive-strip.mjs';
import { verifyClaim } from '../.agents/skills/vercel-optimize/lib/verify-claim.mjs';

test('strip directive name and value at every list position', () => {
  for (const header of [
    'stale-if-error=600, public, s-maxage=60',
    'public, stale-if-error=600, s-maxage=60',
    'public, s-maxage=60, stale-if-error=600',
    'public, stale-if-error = "600", s-maxage=60',
  ]) {
    const rec = { fix: `Cache-Control: ${header}` };
    apply(rec);
    assert.doesNotMatch(rec.fix, /stale-if-error|(?:^|,)\s*=/);
    assert.match(rec.fix, /public/);
    assert.match(rec.fix, /s-maxage=60/);
    assert.doesNotMatch(rec.fix, /,\s*$/);
  }
});

test('all recommendation fields are sanitized without changing honored values', () => {
  const rec = Object.fromEntries(['fix', 'currentBehavior', 'desiredBehavior'].map(
    field => [field, 'Cache-Control: public, stale-if-error=600, max-age=300, s-maxage=60'],
  ));
  apply(rec);
  for (const value of Object.values(rec)) {
    assert.doesNotMatch(value, /stale-if-error|(?:^|,)\s*=/);
    assert.match(value, /max-age=300/);
    assert.match(value, /s-maxage=60/);
  }
});

test('claim verifier rejects orphan values and empty directives', async () => {
  for (const header of ['public, =600, s-maxage=60', '=600, public', 'public,, s-maxage=60']) {
    const result = await verifyClaim({ type: 'cache_control_header_syntax', rec: { fix: `Cache-Control: ${header}` } });
    assert.equal(result.disposition, 'failed');
  }
});

test('sanitized recommendation passes the offline syntax verifier', async () => {
  const rec = { fix: 'Cache-Control: public, stale-if-error=600, s-maxage=60' };
  apply(rec);
  assert.equal((await verifyClaim({ type: 'cache_control_header_syntax', rec })).disposition, 'verified');
});
