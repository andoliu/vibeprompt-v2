export const TOOLS: Record<string, { label: string; badge: string; href: string }> = {
  jev: {
    label: 'Jev',
    badge: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border border-emerald-500/20',
    href: '/jev-prompts/',
  },
  'claude-code': {
    label: 'Claude Code',
    badge: 'bg-orange-500/10 text-orange-700 dark:text-orange-400 border border-orange-500/20',
    href: '/claude-code-prompts/',
  },
  cursor: {
    label: 'Cursor',
    badge: 'bg-blue-500/10 text-blue-700 dark:text-blue-400 border border-blue-500/20',
    href: '/cursor-prompts/',
  },
  lovable: {
    label: 'Lovable',
    badge: 'bg-rose-500/10 text-rose-700 dark:text-rose-400 border border-rose-500/20',
    href: '/lovable-prompts/',
  },
};

export function toolInfo(tool: string) {
  return TOOLS[tool] ?? { label: tool, badge: 'bg-muted text-muted-foreground border border-border', href: '#' };
}
