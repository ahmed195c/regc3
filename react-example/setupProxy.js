const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  // Proxy API requests to Django server
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://192.168.50.6:8000",
      changeOrigin: true,
      pathRewrite: {
        "^/api": "/api", // No rewrite needed, but you could change this if needed
      },
      // Optional: Additional configuration
      onProxyReq: (proxyReq, req, res) => {
        // Add any custom headers here if needed
        // proxyReq.setHeader('X-Special-Header', 'value');
        console.log("Proxying request:", req.url);
      },
      onProxyRes: (proxyRes, req, res) => {
        // Log proxy responses
        console.log("Proxy response:", proxyRes.statusCode, req.url);
      },
      onError: (err, req, res) => {
        console.error("Proxy error:", err);
        res.writeHead(500, {
          "Content-Type": "text/plain",
        });
        res.end(
          "Proxy error: Could not connect to the API server. Please check if the server is running."
        );
      },
    })
  );
};
