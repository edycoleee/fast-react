export function Button({ variant = "primary", children, className = "", ...props }) {
  const buttonClassName = `btn btn-${variant} ${className}`.trim();
  return (
    <button className={buttonClassName} {...props}>
      {children}
    </button>
  );
}
