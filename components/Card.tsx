import React from 'react';
import { tokens } from '../tokens';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  elevated?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, elevated = false, style, ...props }) => {
  return (
    <div
      style={{
        backgroundColor: tokens.colors.gray[50],
        borderRadius: tokens.borderRadius.lg,
        padding: tokens.spacing.lg,
        boxShadow: elevated ? tokens.shadows.md : tokens.shadows.sm,
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
};
