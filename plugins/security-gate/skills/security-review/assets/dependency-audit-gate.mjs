#!/usr/bin/env node
// Dependency audit gate for npm 7+ projects. See references/deployment-gate.md "의존성 예외".
// Blocks every HIGH/CRITICAL advisory unless a valid build/dev-only exception exists
// and no non-breaking fix is available. Exit: 0 pass, 1 block, 2 unverified.
//
// Usage: node dependency-audit-gate.mjs [--exceptions security/dependency-exceptions.json]
//                                       [--audit-json audit.json] [--today YYYY-MM-DD]
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const option = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};

const exceptionsPath = option('--exceptions', 'security/dependency-exceptions.json');
const auditPath = option('--audit-json');
const localDate = (date) =>
  [date.getFullYear(), date.getMonth() + 1, date.getDate()].map((part) => String(part).padStart(2, '0')).join('-');
const today = option('--today', localDate(new Date()));
const MAX_DAYS = 90;
const DAY_MS = 86_400_000;
const BLOCKING = new Set(['high', 'critical']);
const SCOPES = new Set(['build-only', 'dev-only']);

function unverified(message) {
  console.error(`UNVERIFIED: ${message}`);
  process.exit(2);
}

function loadAudit() {
  if (auditPath) return JSON.parse(readFileSync(auditPath, 'utf8'));
  try {
    const output = execFileSync('npm', ['audit', '--json'], {
      encoding: 'utf8',
      maxBuffer: 64 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    return JSON.parse(output);
  } catch (error) {
    // npm audit exits 1 when vulnerabilities exist; the JSON report is still on stdout.
    try {
      return JSON.parse(error.stdout);
    } catch {
      return unverified('npm audit did not return JSON (lockfile, registry or network problem)');
    }
  }
}

function loadExceptions() {
  if (!existsSync(exceptionsPath)) return [];
  try {
    const parsed = JSON.parse(readFileSync(exceptionsPath, 'utf8'));
    if (!Array.isArray(parsed.exceptions)) throw new Error('missing exceptions array');
    return parsed.exceptions;
  } catch {
    return unverified(`cannot read ${exceptionsPath} as { "exceptions": [...] }`);
  }
}

const parseDate = (value) =>
  /^\d{4}-\d{2}-\d{2}$/.test(value ?? '') ? Date.parse(`${value}T00:00:00Z`) : Number.NaN;

const hasNonBreakingFix = (fix) =>
  fix === true || (typeof fix === 'object' && fix !== null && fix.isSemVerMajor === false);

function exceptionProblem(exception) {
  if (!SCOPES.has(exception.scope)) return 'scope must be build-only or dev-only';
  if (!exception.reason || exception.reason.trim().length < 20) {
    return 'reason must explain when the package runs and why attacker input cannot reach it';
  }
  if (!exception.approvedBy) return 'approvedBy is required';
  const approvedAt = parseDate(exception.approvedAt);
  const expires = parseDate(exception.expires);
  if (Number.isNaN(approvedAt) || Number.isNaN(expires)) return 'approvedAt and expires must be YYYY-MM-DD';
  if (expires - approvedAt > MAX_DAYS * DAY_MS) return `expires must be within ${MAX_DAYS} days of approvedAt`;
  if (expires < parseDate(today)) return `expired on ${exception.expires}`;
  return null;
}

const audit = loadAudit();
if (audit.error || audit.advisories || !audit.vulnerabilities) {
  unverified(`unsupported or failed npm audit report${audit.error?.code ? ` (${audit.error.code})` : ''}`);
}

const advisories = new Map();
for (const vulnerability of Object.values(audit.vulnerabilities)) {
  for (const via of vulnerability.via) {
    if (typeof via !== 'object' || !BLOCKING.has(via.severity)) continue;
    const id = via.url?.match(/GHSA(?:-[0-9a-z]{4}){3}/i)?.[0] ?? `npm:${via.source}`;
    const key = `${id}|${via.name}`;
    if (advisories.has(key)) continue;
    advisories.set(key, {
      id,
      packageName: via.name,
      severity: via.severity,
      title: via.title,
      fix: audit.vulnerabilities[via.name]?.fixAvailable,
    });
  }
}

const exceptions = loadExceptions();
const usedExceptions = new Set();
const blocked = [];
const excepted = [];

for (const advisory of advisories.values()) {
  const index = exceptions.findIndex(
    (exception) => exception.id === advisory.id && exception.package === advisory.packageName,
  );
  const fixNote = hasNonBreakingFix(advisory.fix)
    ? 'non-breaking fix available: run npm audit fix (without --force)'
    : null;
  if (index < 0) {
    blocked.push({ ...advisory, why: fixNote ?? 'no exception; fix or add a reviewed build/dev-only exception' });
    continue;
  }
  usedExceptions.add(index);
  const exception = exceptions[index];
  const problem = fixNote ?? exceptionProblem(exception);
  if (problem) blocked.push({ ...advisory, why: `exception rejected: ${problem}` });
  else excepted.push({ ...advisory, scope: exception.scope, expires: exception.expires });
}

const describe = (advisory) =>
  `${advisory.severity.toUpperCase().padEnd(8)} ${advisory.packageName} ${advisory.id} - ${advisory.title}`;

console.log(
  `dependency audit gate (${today}): ${advisories.size} high/critical advisories, ` +
    `${blocked.length} blocked, ${excepted.length} excepted`,
);
for (const advisory of blocked) console.log(`BLOCK   ${describe(advisory)} [${advisory.why}]`);
for (const advisory of excepted) {
  console.log(`EXCEPT  ${describe(advisory)} [${advisory.scope}, expires ${advisory.expires}]`);
}
exceptions.forEach((exception, index) => {
  if (!usedExceptions.has(index)) console.log(`WARN    unused exception ${exception.id} ${exception.package}: remove it`);
});
const counts = audit.metadata?.vulnerabilities;
if (counts) console.log(`INFO    moderate ${counts.moderate}, low ${counts.low}: record impact and schedule`);

process.exit(blocked.length ? 1 : 0);
