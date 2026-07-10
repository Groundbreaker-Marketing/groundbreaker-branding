import React from 'react';
import { tokens } from '../tokens';

interface TypographyProps extends React.HTMLAttributes<HTMLElement> {
  variant: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6' | 'body' | 'caption';
  children: React.ReactNode;
}

const variantMap = {
  h1: { fontSize: tokens.typography.fontSize['5xl'], fontWeight: tokens.typography.fontWeight.bold, lineHeight: tokens.typography.lineHeight.tight },
  h2: { fontSize: tokens.typography.fontSize['4xl'], fontWeight: tokens.typography.fontWeight.bold, lineHeight: tokens.typography.lineHeight.tight },
  h3: { fontSize: tokens.typography.fontSize['3xl'], fontWeight: tokens.typography.fontWeight.semibold, lineHeight: tokens.typography.lineHeight.tight },
  h4: { fontSize: tokens.typography.fontSize['2xl'], fontWeight: tokens.typography.fontWeight.semibold, lineHeight: tokens.typography.lineHeight.normal },
  h5: { fontSize: tokens.typography.fontSize.xl, fontWeight: tokens.typography.fontWeight.semibold, lineHeight: tokens.typography.lineHeight.normal },
  h6: { fontSize: tokens.typography.fontSize.lg, fontWeight: tokens.typography.fontWeight.semibold, lineHeight: tokens.typography.lineHeight.normal },
  body: { fontSize: tokens.typography.fontSize.base, fontWeight: tokens.typography.fontWeight.normal, lineHeight: tokens.typography.lineHeight.normal },
  caption: { fontSize: tokens.typography.fontSize.sm, fontWeight: tokens.typography.fontWeight.normal, lineHeight: tokens.typography.lineHeight.normal, color: tokens.colors.gray[600] },
};

export const Typography: React.FC<TypographyProps> = ({ variant, children, style, ...props }) => {
  const isHeading = variant.startsWith('h');
  const Component = isHeading ? (variant as keyof JSX.IntrinsicElements) : 'p';

  return (
    <Component
      style={{
        fontFamily: isHeading ? tokens.typography.fontFamily.heading : tokens.typography.fontFamily.body,
        ...variantMap[variant],
        color: tokens.colors.gray[900],
        margin: 0,
        ...style,
      }}
      {...props}
    >
      {children}
    </Component>
  );
};
