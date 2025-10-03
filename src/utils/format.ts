export function formatMatchLabel(match: string): string {
  switch (match) {
    case 'exact':
      return 'Exact match';
    case 'partial':
      return 'Partial match';
    case 'mismatch':
      return 'Mismatch';
    case 'missing':
      return 'Missing';
    default:
      return match;
  }
}

export function formatConfidence(confidence: number): string {
  return `${Math.round(confidence * 100)}%`;
}

export function classNameForMatch(match: string): string {
  switch (match) {
    case 'exact':
      return 'bg-success-500/10 text-success-300 border-success-500/40';
    case 'partial':
      return 'bg-warning-500/10 text-warning-300 border-warning-500/40';
    case 'mismatch':
      return 'bg-danger-500/10 text-danger-300 border-danger-500/40';
    case 'missing':
      return 'bg-slate-500/20 text-slate-200 border-slate-400/40';
    default:
      return 'bg-slate-500/20 text-slate-100 border-slate-400/30';
  }
}

export function formatRisk(risk: string): string {
  return risk.charAt(0) + risk.slice(1).toLowerCase();
}
