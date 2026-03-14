import * as React from 'react';
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'neon' | 'purple';
    hover?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
    ({ className, variant = 'default', hover = true, ...props }, ref) => {
        const variants = {
            default: 'glass border border-border rounded-xl',
            neon: 'glass-neon rounded-xl',
            purple: 'glass-purple rounded-xl',
        };
        return (
            <div
                ref={ref}
                className={cn(variants[variant], hover && 'transition-all duration-300 hover:border-neon/20 hover:shadow-glass', className)}
                {...props}
            />
        );
    }
);
Card.displayName = 'Card';

const CardHeader = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn('flex flex-col gap-1.5 p-6', className)} {...props} />
);

const CardTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
    <h3 className={cn('text-lg font-semibold text-text-primary', className)} {...props} />
);

const CardContent = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn('px-6 pb-6', className)} {...props} />
);

const CardFooter = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
    <div className={cn('px-6 pb-6 flex items-center gap-4', className)} {...props} />
);

export { Card, CardHeader, CardTitle, CardContent, CardFooter };
