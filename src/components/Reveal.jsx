import { useReveal } from '@/hooks/useReveal.js'

function Reveal({ as: Tag = 'div', className = '', delay = 0, children }) {
  const [ref, visible] = useReveal()

  return (
    <Tag
      ref={ref}
      className={`reveal${visible ? ' reveal-visible' : ''}${className ? ` ${className}` : ''}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </Tag>
  )
}

export default Reveal
