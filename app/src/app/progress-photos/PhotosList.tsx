"use client";
// Your saved progress photos. Only on this device, and you can delete them (Later-AC4, AC5).
/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import { useState } from "react";
import { deleteProgressPhoto, useProgressPhotos } from "@/lib/useProgressPhotos";

export default function PhotosList() {
  const { loaded, photos } = useProgressPhotos();
  const [confirming, setConfirming] = useState<string | null>(null);
  if (!loaded) return <p className="p-4 text-sm text-gray-600">Loading...</p>;
  return (
    <main className="mx-auto max-w-sm space-y-3 p-4">
      <h1 className="text-xl font-semibold">Progress photos</h1>
      <p className="text-sm text-gray-600">Only you can see these. They stay on this device until you delete them.</p>
      {photos.length === 0 && <p className="rounded-xl bg-gray-50 p-4 text-sm">No progress photos yet.</p>}
      <ul className="space-y-3">
        {photos.map((p) => (
          <li key={p.id} className="rounded-xl border p-2">
            <img src={p.image} alt={`Progress photo from ${p.date}`} className="w-full rounded-lg" />
            <div className="mt-2 flex items-center justify-between text-sm">
              <span>{p.date}</span>
              {confirming === p.id ? (
                <span className="flex gap-2">
                  <button className="min-h-11 rounded-lg bg-gray-200 px-3" onClick={() => setConfirming(null)}>Keep</button>
                  <button className="min-h-11 rounded-lg bg-red-700 px-3 text-white" onClick={() => { deleteProgressPhoto(p.id); setConfirming(null); }}>Delete for good</button>
                </span>
              ) : (
                <button className="min-h-11 rounded-lg px-3 text-red-700 underline" onClick={() => setConfirming(p.id)}>Delete</button>
              )}
            </div>
          </li>
        ))}
      </ul>
      <Link href="/" className="inline-flex min-h-12 items-center rounded-xl bg-gray-200 px-4 font-semibold">Back to Today</Link>
    </main>
  );
}
