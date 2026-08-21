export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (request.method !== "GET") {
      return new Response("method not allowed\n", { status: 405 });
    }
    if (url.pathname === "/healthz") {
      return Response.json({
        component: "zoracleflux-health-adapter",
        runtime: "cloudflare-worker-reference",
        status: "ok",
        customer_data: false,
      });
    }
    if (url.pathname === "/") {
      return new Response(
        "Reference adapter only; GitHub Pages/Actions do not host the API.\n",
        { headers: { "content-type": "text/plain; charset=utf-8" } },
      );
    }
    return new Response("not found\n", { status: 404 });
  },
};
