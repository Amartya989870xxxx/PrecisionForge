"use client";
import { useState } from "react";
import { Field } from "@/components/ui/Field";
import { Button } from "@/components/ui/Button";
export function ContactForm() {
  const [err, setErr] = useState("");
  const [sent, setSent] = useState(false);
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    if (!fd.get("name") || !fd.get("email") || !fd.get("message")) { setErr("Please complete all fields."); return; }
    setErr("");
    const endpoint = process.env.NEXT_PUBLIC_CONTACT_ENDPOINT;
    if (endpoint) await fetch(endpoint, { method: "POST", body: fd }).catch(() => {});
    setSent(true);
  }
  if (sent) return <p className="text-accent">Thanks — we’ll be in touch.</p>;
  return (
    <form onSubmit={onSubmit} noValidate className="space-y-5">
      <Field label="Name" name="name" required />
      <Field label="Email" name="email" type="email" required />
      <Field label="Message" name="message" textarea required />
      {err && <p className="text-sm text-accent">{err}</p>}
      <Button type="submit">Send message</Button>
    </form>
  );
}
