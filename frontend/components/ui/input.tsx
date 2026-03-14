import * as React from 'react';
import { cn } from '@/lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, label, error, id, ...props }, ref) => (
        <div className="flex flex-col gap-1.5">
            {label && <label htmlFor={id} className="text-sm font-medium text-text-secondary">{label}</label>}
            <input
                ref={ref}
                id={id}
                className={cn(
                    'input-cyber',
                    error && 'border-danger/50 focus:border-danger focus:shadow-[0_0_0_3px_rgba(255,50,50,0.1)]',
                    className
                )}
                {...props}
            />
            {error && <p className="text-xs text-danger">{error}</p>}
        </div>
    )
);
Input.displayName = 'Input';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    error?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, label, error, id, ...props }, ref) => (
        <div className="flex flex-col gap-1.5">
            {label && <label htmlFor={id} className="text-sm font-medium text-text-secondary">{label}</label>}
            <textarea
                ref={ref}
                id={id}
                className={cn(
                    'input-cyber resize-none',
                    error && 'border-danger/50 focus:border-danger',
                    className
                )}
                {...props}
            />
            {error && <p className="text-xs text-danger">{error}</p>}
        </div>
    )
);
Textarea.displayName = 'Textarea';

export { Input, Textarea };
