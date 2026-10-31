// Cloudflare Pages Function: receives the "build an AI automation" form
// and stores it in Systeme.io as a contact with a "Build enquiry" field.
// Needs one encrypted environment variable in Cloudflare Pages:
//   SYSTEME_API_KEY  (created in Systeme.io > Settings > MCP & API keys)

const API = "https://api.systeme.io/api";
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

    // Tag the contact "build-enquiry" (tag already exists in Systeme; free plan allows one tag).
    const tags = await (await call("/tags?limit=100")).json();
    const tag = (tags.items || []).find((t) => t.name === "build-enquiry");
    if (tag) await call(`/contacts/${contact.id}/tags`, "POST", { tagId: tag.id });

    // Instant alert to Constantin: phone push (ntfy app, topic below) + email to hello@ (forwards to Gmail).
    try {
      await fetch(`https://ntfy.sh/${env.NTFY_TOPIC || "uaiwm-leads-b36a69a28c42"}`, {
        method: "POST",
        headers: {
          Title: "New build enquiry",
          Tags: "moneybag",
          Priority: "high",
          Email: "hello@understandaiwithme.com",
          Click: "https://systeme.io/dashboard/contacts",
        },
        // No name/email here (third-party service): details are in Systeme > Contacts > tag build-enquiry.
        body: `Team size: ${form.get("team_size") || "-"}\nHours per week: ${String(form.get("hours") || "-").slice(0, 40)}\nBudget: ${form.get("budget") || "-"}\nTiming: ${form.get("timing") || "-"}\n\nOpen Systeme Contacts (tag: build-enquiry) for the name, email and task. Reply within a day, then pass to Digital One quoting REF-CONSTANT266.`,
      });
    } catch (e) {
      // never block the visitor on a failed alert
    }

    return redirect(request, "thanks");
  } catch (err) {
    return redirect(request, "error");
  }
}

function redirect(request, page) {
  return Response.redirect(new URL(`/fix/build-ai-automation/${page}/`, request.url), 303);
}
