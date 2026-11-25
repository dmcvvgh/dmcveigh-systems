// Eaten versus burned for the days of this week so far (S3-AC6). Plain SVG, no chart library.
const LETTERS = ["S", "M", "T", "W", "T", "F", "S"];
const W = 300;
const H = 120;
const PAD = { left: 8, right: 8, top: 8, bottom: 20 };

function path(values: (number | null)[], max: number): string {
  const step = (W - PAD.left - PAD.right) / 6;
  return values
    .map((v, i) => (v === null ? null : `${PAD.left + i * step},${PAD.top + (1 - v / max) * (H - PAD.top - PAD.bottom)}`))
    .filter(Boolean)
    .join(" ");
}

export default function WeekChart({
  eaten,
  burned,
  todayIndex,
}: {
  eaten: (number | null)[];
  burned: (number | null)[];
  todayIndex: number;
}) {
  const max = Math.max(1, ...eaten.map((v) => v ?? 0), ...burned.map((v) => v ?? 0)) * 1.1;
  const step = (W - PAD.left - PAD.right) / 6;
  const summary = `Eaten versus burned, days so far this week. Today: ${eaten[todayIndex] ?? 0} eaten, ${burned[todayIndex] ?? 0} burned.`;
  return (
    <figure className="mt-3">
      <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={summary} className="w-full rounded-lg bg-gray-50">
        {LETTERS.map((l, i) => (
          <text key={i} x={PAD.left + i * step} y={H - 5} fontSize="10" textAnchor="middle" fill={i === todayIndex ? "#15803d" : "#6b7280"} fontWeight={i === todayIndex ? 700 : 400}>
            {l}
          </text>
        ))}
        <polyline fill="none" stroke="#e08e45" strokeWidth="3" strokeLinejoin="round" points={path(burned, max)} />
        <polyline fill="none" stroke="#2e8b57" strokeWidth="3" strokeLinejoin="round" points={path(eaten, max)} />
        {eaten.map((v, i) =>
          v === null ? null : (
            <circle key={i} cx={PAD.left + i * step} cy={PAD.top + (1 - v / max) * (H - PAD.top - PAD.bottom)} r="3" fill="#2e8b57" />
          ),
        )}
      </svg>
      <figcaption className="mt-1 flex gap-3 text-xs text-gray-600">
        <span><i className="mr-1 inline-block h-2.5 w-2.5 rounded-sm bg-[#e08e45]" />Burned</span>
        <span><i className="mr-1 inline-block h-2.5 w-2.5 rounded-sm bg-[#2e8b57]" />Eaten</span>
        <span>This week so far</span>
      </figcaption>
    </figure>
  );
}
