// Cloudflare Pages Function: receives the "build an AI automation" form
// and stores it in Systeme.io as a contact tagged "build-enquiry".
// Needs one encrypted environment variable in Cloudflare Pages:
//   SYSTEME_API_KEY  (created in Systeme.io > Settings > MCP & API keys)

const API = "https://api.systeme.io/api";
const TAG = "build-enquiry";
const FIELD = { name: "Build enquiry", slug: "build_enquiry" };

export async function onRequestPost({ request, env }) {
  const form = await request.formData();
  if (form.get("website")) return redirect(request, "thanks"); // honeypot: bots fill it

  const email = String(form.get("email") || "").trim();
  const name = String(form.get("name") || "").trim().slice(0, 100);
  if (!email.includes("@")) return redirect(request, "error");

  const summary = [
    `Team size: ${form.get("team_size") || "-"}`,
    `Task: ${String(form.get("task") || "-").slice(0, 2000)}`,
    `Hours per week: ${form.get("hours") || "-"}`,
    `Budget: ${form.get("budget") || "-"}`,
    `Timing: ${form.get("timing") || "-"}`,
    `Submitted: ${new Date().toISOString()}`,
  ].join("\n");

  if (!env.SYSTEME_API_KEY) return redirect(request, "error");
  const call = (path, method = "GET", body) =>
    fetch(API + path, {
      method,
      headers: {
        "X-API-Key": env.SYSTEME_API_KEY,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: body ? JSON.stringify(body) : undefined,
    });

  try {
    // Make sure the custom field exists (fails harmlessly if it already does).
    await call("/contact_fields", "POST", { fieldName: FIELD.name, name: FIELD.name, slug: FIELD.slug });

    const fields = [
      { slug: "first_name", value: name },
      { slug: FIELD.slug, value: summary },
    ];
    let res = await call("/contacts", "POST", { email, locale: "en", fields });
    let contact = res.ok ? await res.json() : null;

    if (!contact) {
      // Existing contact: find it and update the enquiry field.
      const found = await (await call(`/contacts?email=${encodeURIComponent(email)}`)).json();
      contact = (found.items || [])[0];
      if (!contact) return redirect(request, "error");
      await fetch(`${API}/contacts/${contact.id}`, {
        method: "PATCH",
        headers: {
          "X-API-Key": env.SYSTEME_API_KEY,
          "Content-Type": "application/merge-patch+json",
        },
        body: JSON.stringify({ fields }),
      });
    }

    const tags = await (await call("/tags?limit=100")).json();
    let tag = (tags.items || []).find((t) => t.name === TAG);
    if (!tag) tag = await (await call("/tags", "POST", { name: TAG })).json();
    if (tag && tag.id) await call(`/contacts/${contact.id}/tags`, "POST", { tagId: tag.id });

    return redirect(request, "thanks");
  } catch (err) {
    return redirect(request, "error");
  }
}

function redirect(request, page) {
  return Response.redirect(new URL(`/fix/build-ai-automation/${page}/`, request.url), 303);
}
