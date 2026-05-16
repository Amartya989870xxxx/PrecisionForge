import { useEffect, useRef, useState } from 'react';
import { useInView, useMotionValue, useSpring } from 'framer-motion';

export default function StatCounter({ from = 0, to = 100, suffix = '', duration = 1500, decimals = 2 }) {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '-50px' });
  const [displayValue, setDisplayValue] = useState(from.toFixed(decimals));
  
  const motionValue = useMotionValue(from);
  const springValue = useSpring(motionValue, {
    duration: duration,
    bounce: 0,
    restDelta: 0.001
  });

  useEffect(() => {
    if (inView) {
      motionValue.set(to);
    }
  }, [inView, motionValue, to]);

  useEffect(() => {
    return springValue.on('change', (latest) => {
      // Determine format based on 'to' value type (integer or float)
      const isInteger = to % 1 === 0 && from % 1 === 0;
      setDisplayValue(isInteger ? Math.round(latest).toString() : latest.toFixed(decimals));
    });
  }, [springValue, to, from, decimals]);

  return (
    <span ref={ref}>
      {displayValue}{suffix}
    </span>
  );
}
