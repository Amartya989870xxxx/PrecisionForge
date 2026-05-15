export function Container({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={`mx-auto w-full max-w-container px-[var(--side-pad)] ${className}`}>{children}</div>
  );
}
