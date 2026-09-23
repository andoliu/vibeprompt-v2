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
  v0: {
    label: 'v0',
    badge: 'bg-neutral-500/10 text-neutral-700 dark:text-neutral-300 border border-neutral-500/20',
    href: '/v0-prompts/',
  },
  bolt: {
    label: 'Bolt',
    badge: 'bg-violet-500/10 text-violet-700 dark:text-violet-400 border border-violet-500/20',
    href: '/bolt-prompts/',
  },
  windsurf: {
    label: 'Windsurf',
    badge: 'bg-teal-500/10 text-teal-700 dark:text-teal-400 border border-teal-500/20',
    href: '/windsurf-prompts/',
  },
};

export function toolInfo(tool: string) {
  return TOOLS[tool] ?? { label: tool, badge: 'bg-muted text-muted-foreground border border-border', href: '#' };
}
