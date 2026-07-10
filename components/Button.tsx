import React from 'react';
import { tokens } from '../tokens';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'tertiary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  ...props
}) => {
  const baseStyles: React.CSSProperties = {
    fontFamily: tokens.typography.fontFamily.heading,
    fontWeight: tokens.typography.fontWeight.semibold,
    borderRadius: tokens.borderRadius.md,
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  };

  const sizeStyles: Record<string, React.CSSProperties> = {
    sm: {
      fontSize: tokens.typography.fontSize.sm,
      padding: `${tokens.spacing.sm} ${tokens.spacing.md}`,
    },
    md: {
      fontSize: tokens.typography.fontSize.base,
      padding: `${tokens.spacing.md} ${tokens.spacing.lg}`,
    },
    lg: {
      fontSize: tokens.typography.fontSize.lg,
      padding: `${tokens.spacing.lg} ${tokens.spacing.xl}`,
    },
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: {
      backgroundColor: tokens.colors.primary[700],
      color: 'white',
    },
    secondary: {
      backgroundColor: tokens.colors.accent[600],
      color: tokens.colors.primary[900],
    },
    tertiary: {
      backgroundColor: 'transparent',
      color: tokens.colors.primary[700],
      border: `2px solid ${tokens.colors.primary[700]}`,
    },
  };

  return (
    <button
      style={{
        ...baseStyles,
        ...sizeStyles[size],
        ...variantStyles[variant],
      }}
      {...props}
    >
      {children}
    </button>
  );
};
