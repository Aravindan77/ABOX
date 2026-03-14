import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'neon' | 'outline' | 'ghost' | 'destructive' | 'purple';
    size?: 'sm' | 'md' | 'lg';
    loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'neon', size = 'md', loading, children, disabled, ...props }, ref) => {
        const base = 'inline-flex items-center justify-center gap-2 font-semibold rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed';
        const sizes = {
            sm: 'px-4 py-2 text-xs',
            md: 'px-6 py-3 text-sm',
            lg: 'px-8 py-4 text-base',
        };
        const variants = {
            neon: 'bg-neon-gradient text-background hover:shadow-neon hover:-translate-y-0.5',
            outline: 'border border-neon/40 text-neon hover:bg-neon/10 hover:border-neon hover:shadow-neon',
            ghost: 'text-text-secondary hover:text-text-primary hover:bg-white/5',
            destructive: 'bg-danger/20 text-danger border border-danger/30 hover:bg-danger/30',
            purple: 'bg-purple-gradient text-white hover:shadow-purple hover:-translate-y-0.5',
        };
        return (
            <button
                ref={ref}
                className={cn(base, sizes[size], variants[variant], className)}
                disabled={disabled || loading}
                {...props}
            >
                {loading && (
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                )}
                {children}
            </button>
        );
    }
);
Button.displayName = 'Button';
export { Button };
