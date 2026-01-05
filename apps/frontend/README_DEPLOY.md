# EduPredict Frontend — Cloudflare Pages (Free)

This frontend is a **Next.js** app.

## Cloudflare Pages setup

1. Create a new **Pages** project.
2. Connect it to your GitHub repo.
3. Set these build settings:
   - **Root directory:** `apps/frontend`
   - **Build command:** `npm run build`
  - **Output directory:** `out`

Cloudflare Pages will usually auto-detect Next.js.

This project is configured for **static export** on Pages (`output: "export"`), which avoids uploading large `.next/cache` artifacts that can exceed Cloudflare Pages’ per-file size limit.

## Environment variables

Set this in Cloudflare Pages → Settings → Environment variables:

- `NEXT_PUBLIC_API_BASE_URL` = your deployed backend URL
  - Example: `https://<your-space>.hf.space`

## Notes

- The frontend calls the backend at runtime using `NEXT_PUBLIC_API_BASE_URL`.
- After you deploy the backend, update this variable and redeploy the Pages project.
