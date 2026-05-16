"use client";
import Link from "next/link";

export interface ButtonProps {
  href?: string;
  variant?: "primary" | "ghost";
  children: React.ReactNode;
  onClick?: () => void;
  type?: "button" | "submit";
}

export function Button({ href, variant = "primary", children, onClick, type = "button" }: ButtonProps) {
  const cls = `inline-block rounded-md px-6 py-3 font-medium transition-colors duration-300 ease-brand ${variant === "primary" ? "bg-accent text-bg hover:bg-accent-2" : "border border-border text-text hover:bg-surface"}`;
  if (href) return <Link href={href} className={cls}>{children}</Link>;
  return <button type={type} onClick={onClick} className={cls}>{children}</button>;
}
