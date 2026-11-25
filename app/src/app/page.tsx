import { appName } from "@/lib/hello";

export default function Home() {
  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-xl font-semibold">{appName()}</h1>
      <p className="text-sm text-gray-600">Hello. v1 is being built.</p>
    </main>
  );
}
