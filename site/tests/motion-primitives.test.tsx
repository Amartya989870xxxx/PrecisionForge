import { render, screen, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeAll, afterEach } from "vitest";
import { Reveal } from "@/motion/Reveal";
import { CountUp } from "@/motion/CountUp";
import { Stagger, StaggerItem } from "@/motion/Stagger";

type IOCallback = (entries: { isIntersecting: boolean }[]) => void;

// Capture constructed IntersectionObserver instances so tests can fire the callback.
let lastIO: { cb: IOCallback; observe: () => void; disconnect: () => void } | null = null;

// Local IntersectionObserver shim (do NOT edit shared vitest.setup.ts)
beforeAll(() => {
  function IO(this: { cb: IOCallback }, cb: IOCallback) {
    const instance = {
      cb,
      observe() {},
      disconnect() {},
      unobserve() {},
    };
    lastIO = instance;
    return instance;
  }
  window.IntersectionObserver =
    window.IntersectionObserver || (IO as unknown as typeof IntersectionObserver);
});

function setReducedMotion(matches: boolean) {
  window.matchMedia = ((q: string) => ({
    matches,
    media: q,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })) as never;
}

// Restore matchMedia to the matches:false mock after every test (prevent shared-state bleed).
afterEach(() => {
  setReducedMotion(false);
  lastIO = null;
  vi.restoreAllMocks();
});

describe("motion primitives", () => {
  it("Reveal renders its children", () => {
    render(<Reveal><span>revealed</span></Reveal>);
    expect(screen.getByText("revealed")).toBeInTheDocument();
  });

  it("Reveal under reduced motion renders a plain div", () => {
    setReducedMotion(true);
    const { container } = render(<Reveal className="rv"><span>r</span></Reveal>);
    const el = container.querySelector("div.rv");
    expect(el).toBeInTheDocument();
    expect(screen.getByText("r")).toBeInTheDocument();
  });

  it("CountUp shows final value under reduced motion", () => {
    setReducedMotion(true);
    render(<CountUp to={70.22} suffix=" / 90" />);
    expect(screen.getByText(/70\.22 \/ 90/)).toBeInTheDocument();
  });

  it("CountUp animates to the final value when intersecting", () => {
    setReducedMotion(false);
    let raf = 0;
    const rafSpy = vi
      .spyOn(window, "requestAnimationFrame")
      .mockImplementation((cb: FrameRequestCallback) => {
        raf += 1;
        // Fire immediately with a timestamp far beyond the 900ms duration.
        cb(raf === 1 ? 0 : 5000);
        return raf;
      });
    vi.spyOn(window, "cancelAnimationFrame").mockImplementation(() => {});

    render(<CountUp to={42} prefix="$" decimals={0} />);
    expect(lastIO).not.toBeNull();
    act(() => {
      lastIO!.cb([{ isIntersecting: true }]);
    });
    expect(screen.getByText(/\$42/)).toBeInTheDocument();
    rafSpy.mockRestore();
  });

  it("CountUp ignores a non-intersecting entry", () => {
    setReducedMotion(false);
    render(<CountUp to={10} decimals={0} />);
    expect(lastIO).not.toBeNull();
    act(() => {
      lastIO!.cb([{ isIntersecting: false }]);
    });
    expect(screen.getByText(/^0$/)).toBeInTheDocument();
  });

  it("Stagger + StaggerItem render their children (non-reduced)", () => {
    setReducedMotion(false);
    render(
      <Stagger className="st">
        <StaggerItem className="it"><span>child-a</span></StaggerItem>
        <StaggerItem><span>child-b</span></StaggerItem>
      </Stagger>,
    );
    expect(screen.getByText("child-a")).toBeInTheDocument();
    expect(screen.getByText("child-b")).toBeInTheDocument();
  });

  it("Stagger renders a plain div under reduced motion", () => {
    setReducedMotion(true);
    const { container } = render(
      <Stagger className="stg">
        <StaggerItem><span>only</span></StaggerItem>
      </Stagger>,
    );
    expect(container.querySelector("div.stg")).toBeInTheDocument();
    expect(screen.getByText("only")).toBeInTheDocument();
  });
});
