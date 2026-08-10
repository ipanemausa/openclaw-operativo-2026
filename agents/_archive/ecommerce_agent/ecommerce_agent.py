"""
================================================================
  ecommerce_agent.py — OpenClaw E-Commerce Integration Agent
  HBJewelry 2026.7.1

  Conecta el catálogo HBJewelry con:
  - Shopify Admin API 2024-01
  - WooCommerce REST API v3
  - Webhooks bidireccionales → intent-server.js
================================================================
"""

import os
import json
import hmac
import hashlib
import logging
import httpx
from datetime import datetime
from typing import Optional

logger = logging.getLogger("ecommerce_agent")

# ─── Config ──────────────────────────────────────────────────────────────────

SHOPIFY_SHOP    = os.getenv("SHOPIFY_SHOP_DOMAIN", "")       # ej: hbjewelry.myshopify.com
SHOPIFY_TOKEN   = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
SHOPIFY_SECRET  = os.getenv("SHOPIFY_WEBHOOK_SECRET", "")
SHOPIFY_BASE    = f"https://{SHOPIFY_SHOP}/admin/api/2024-01"

WC_URL          = os.getenv("WC_STORE_URL", "")              # ej: https://hbjewelry.com
WC_KEY          = os.getenv("WC_CONSUMER_KEY", "")
WC_SECRET       = os.getenv("WC_CONSUMER_SECRET", "")
WC_BASE         = f"{WC_URL}/wp-json/wc/v3"

OPENCLAW_WEBHOOK_BASE = os.getenv("OPENCLAW_PUBLIC_URL", "http://localhost:3001")

# ─── Shopify Connector ────────────────────────────────────────────────────────

class ShopifyConnector:
    """
    Sincroniza productos HBJewelry ↔ Shopify.
    Usa la Shopify Admin REST API 2024-01.
    """

    def __init__(self):
        self.headers = {
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type": "application/json",
        }

    async def sync_product(self, hb_product: dict) -> dict:
        """Crea o actualiza un producto en Shopify."""
        shopify_id = hb_product.get("shopify_product_id")
        payload    = self._to_shopify_payload(hb_product)

        async with httpx.AsyncClient() as client:
            if shopify_id:
                # Actualizar producto existente
                r = await client.put(
                    f"{SHOPIFY_BASE}/products/{shopify_id}.json",
                    json=payload, headers=self.headers, timeout=30
                )
            else:
                # Crear nuevo producto
                r = await client.post(
                    f"{SHOPIFY_BASE}/products.json",
                    json=payload, headers=self.headers, timeout=30
                )

            r.raise_for_status()
            data = r.json()
            logger.info(f"[Shopify] Product synced: {data['product']['id']}")
            return data["product"]

    async def update_inventory(self, shopify_variant_id: str, qty: int, location_id: str) -> bool:
        """Actualiza el stock de una variante en Shopify."""
        payload = {
            "location_id": location_id,
            "inventory_item_id": shopify_variant_id,
            "available": qty,
        }
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{SHOPIFY_BASE}/inventory_levels/set.json",
                json=payload, headers=self.headers, timeout=20
            )
            r.raise_for_status()
            logger.info(f"[Shopify] Inventory updated: variant={shopify_variant_id} qty={qty}")
            return True

    async def get_orders(self, since: Optional[str] = None, status: str = "any") -> list:
        """Obtiene pedidos de Shopify."""
        params = {"status": status, "limit": 50}
        if since:
            params["created_at_min"] = since

        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{SHOPIFY_BASE}/orders.json",
                params=params, headers=self.headers, timeout=30
            )
            r.raise_for_status()
            return r.json().get("orders", [])

    async def register_webhooks(self) -> list:
        """Registra todos los webhooks de Shopify apuntando al intent-server."""
        topics = [
            ("orders/create",         f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/order_created"),
            ("orders/paid",           f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/order_paid"),
            ("orders/cancelled",      f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/order_cancelled"),
            ("inventory_levels/update",f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/inventory_update"),
            ("products/create",       f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/product_created"),
            ("products/update",       f"{OPENCLAW_WEBHOOK_BASE}/webhooks/shopify/product_updated"),
        ]

        results = []
        async with httpx.AsyncClient() as client:
            for topic, url in topics:
                payload = {"webhook": {"topic": topic, "address": url, "format": "json"}}
                r = await client.post(
                    f"{SHOPIFY_BASE}/webhooks.json",
                    json=payload, headers=self.headers, timeout=20
                )
                if r.status_code in (200, 201, 422):  # 422 = ya existe
                    logger.info(f"[Shopify] Webhook registered: {topic}")
                    results.append({"topic": topic, "url": url, "status": "ok"})
        return results

    def verify_webhook(self, body: bytes, hmac_header: str) -> bool:
        """Verifica la firma HMAC de un webhook de Shopify."""
        digest = hmac.new(SHOPIFY_SECRET.encode(), body, hashlib.sha256).digest()
        import base64
        computed = base64.b64encode(digest).decode()
        return hmac.compare_digest(computed, hmac_header)

    def _to_shopify_payload(self, p: dict) -> dict:
        """Mapea el producto HBJewelry al formato Shopify."""
        metal_desc = f"{p['metal']['tipo']} {p['metal']['quilates']}K"
        gems_desc  = ", ".join(f"{g['tipo']} {g['quilates_ct']}ct" for g in p.get("gemas", []))

        tags = list(set(
            (p.get("seo", {}).get("tags") or []) +
            [metal_desc] +
            [g["tipo"] for g in p.get("gemas", [])] +
            [p.get("categoria", "")]
        ))

        variants = []
        for v in p.get("variantes", []):
            variant = {
                "sku":                  f"{p['sku']}-{v['id']}",
                "price":                f"{v.get('precio_usd', 0):.2f}",
                "inventory_management": "shopify",
                "inventory_quantity":   v.get("stock", 0),
                "weight":               p["metal"].get("peso_gramos", 0),
                "weight_unit":          "g",
                "option1": f"{v['talla_mm']}mm" if v.get("talla_mm") else v.get("acabado", ""),
            }
            if v.get("shopify_variant_id"):
                variant["id"] = v["shopify_variant_id"]
            variants.append(variant)

        options = []
        if any(v.get("talla_mm") for v in p.get("variantes", [])):
            options.append({
                "name": "Talla",
                "values": list(set(f"{v['talla_mm']}mm" for v in p["variantes"] if v.get("talla_mm")))
            })
        else:
            options.append({
                "name": "Acabado",
                "values": list(set(v.get("acabado", "Pulido") for v in p.get("variantes", [])))
            })

        return {
            "product": {
                "title":        p["nombre"],
                "body_html":    p.get("descripcion", ""),
                "vendor":       p.get("marca", "HB Jewelry"),
                "product_type": p.get("categoria", ""),
                "tags":         ",".join(tags),
                "status":       "active" if p.get("publicado") else "draft",
                "variants":     variants,
                "options":      options,
                "images":       [{"src": img["url"], "alt": img.get("alt", p["nombre"])} for img in p.get("imagenes", [])],
            }
        }


# ─── WooCommerce Connector ────────────────────────────────────────────────────

class WooCommerceConnector:
    """
    Sincroniza productos HBJewelry ↔ WooCommerce.
    Usa WooCommerce REST API v3 con autenticación básica HTTPS.
    """

    def __init__(self):
        self.auth = (WC_KEY, WC_SECRET)

    async def sync_product(self, hb_product: dict) -> dict:
        """Crea o actualiza un producto en WooCommerce."""
        wc_id   = hb_product.get("woocommerce_product_id")
        payload = self._to_wc_payload(hb_product)

        async with httpx.AsyncClient() as client:
            if wc_id:
                r = await client.put(f"{WC_BASE}/products/{wc_id}", json=payload, auth=self.auth, timeout=30)
            else:
                r = await client.post(f"{WC_BASE}/products", json=payload, auth=self.auth, timeout=30)
            r.raise_for_status()
            data = r.json()
            logger.info(f"[WooCommerce] Product synced: {data['id']}")
            return data

    async def update_stock(self, wc_product_id: str, qty: int) -> bool:
        """Actualiza el stock de un producto en WooCommerce."""
        async with httpx.AsyncClient() as client:
            r = await client.put(
                f"{WC_BASE}/products/{wc_product_id}",
                json={"stock_quantity": qty, "manage_stock": True},
                auth=self.auth, timeout=20
            )
            r.raise_for_status()
            logger.info(f"[WooCommerce] Stock updated: id={wc_product_id} qty={qty}")
            return True

    async def get_orders(self, status: str = "any") -> list:
        """Obtiene pedidos de WooCommerce."""
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{WC_BASE}/orders", params={"status": status, "per_page": 50}, auth=self.auth, timeout=30)
            r.raise_for_status()
            return r.json()

    def _to_wc_payload(self, p: dict) -> dict:
        """Mapea el producto HBJewelry al formato WooCommerce."""
        meta_data = [
            {"key": "_hb_metal_tipo",     "value": p["metal"]["tipo"]},
            {"key": "_hb_metal_quilates", "value": str(p["metal"]["quilates"])},
            {"key": "_hb_peso_gramos",    "value": str(p["metal"].get("peso_gramos", 0))},
            {"key": "_hb_personalizable", "value": "yes" if p.get("personalizable") else "no"},
        ]
        for i, g in enumerate(p.get("gemas", [])):
            meta_data += [
                {"key": f"_hb_gema_{i}_tipo",     "value": g["tipo"]},
                {"key": f"_hb_gema_{i}_ct",       "value": str(g["quilates_ct"])},
                {"key": f"_hb_gema_{i}_claridad", "value": g.get("claridad", "")},
                {"key": f"_hb_gema_{i}_cert",     "value": g.get("certificado", "")},
            ]

        return {
            "name":          p["nombre"],
            "type":          "variable" if len(p.get("variantes", [])) > 1 else "simple",
            "status":        "publish" if p.get("publicado") else "draft",
            "description":   p.get("descripcion", ""),
            "sku":           p["sku"],
            "regular_price": str(p.get("precio_base_usd", 0)),
            "categories":    [{"name": p.get("categoria", "")}],
            "tags":          [{"name": t} for t in (p.get("seo", {}).get("tags") or [])],
            "images":        [{"src": img["url"]} for img in p.get("imagenes", [])],
            "manage_stock":  True,
            "stock_quantity": p.get("stock_total", 0),
            "meta_data":     meta_data,
        }


# ─── Webhook Handler ──────────────────────────────────────────────────────────

class EcommerceWebhookHandler:
    """
    Procesa webhooks entrantes de Shopify y WooCommerce.
    Se integra con el intent-server.js via SSE / cola interna.
    """

    def __init__(self):
        self.shopify = ShopifyConnector()
        self.woo     = WooCommerceConnector()

    async def handle_shopify(self, topic: str, payload: dict) -> dict:
        """Procesa un webhook de Shopify."""
        logger.info(f"[Webhook] Shopify topic={topic}")

        if topic == "orders/create" or topic == "orders/paid":
            return await self._handle_order(payload, source="shopify")

        if topic == "inventory_levels/update":
            return await self._handle_inventory_update(payload, source="shopify")

        if topic in ("products/create", "products/update"):
            return await self._handle_product_sync(payload, source="shopify")

        return {"status": "ignored", "topic": topic}

    async def handle_woocommerce(self, event: str, payload: dict) -> dict:
        """Procesa un webhook de WooCommerce."""
        logger.info(f"[Webhook] WooCommerce event={event}")

        if event in ("order.created", "order.payment_complete"):
            return await self._handle_order(payload, source="woocommerce")

        if event == "product.updated":
            return await self._handle_product_sync(payload, source="woocommerce")

        return {"status": "ignored", "event": event}

    async def _handle_order(self, order: dict, source: str) -> dict:
        """
        Cuando llega un pedido nuevo:
        1. Decrementar stock en Inventario
        2. Crear entrada en Facturación (cobrado)
        3. Notificar WhatsApp al cliente
        4. Crear evento SSE para el frontend
        """
        order_id    = order.get("id") or order.get("order_key")
        customer    = order.get("billing_address") or order.get("billing", {})
        total       = order.get("total_price") or order.get("total")
        line_items  = order.get("line_items", [])

        logger.info(f"[Order] Nueva orden {order_id} de {source} · Total: ${total}")

        # Evento para el frontend (SSE via intent-server)
        event_payload = {
            "type":      "order_new",
            "source":    source,
            "order_id":  str(order_id),
            "total_usd": float(total or 0),
            "customer":  f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip(),
            "items":     len(line_items),
            "timestamp": datetime.utcnow().isoformat(),
        }

        return {"status": "processed", "event": event_payload}

    async def _handle_inventory_update(self, payload: dict, source: str) -> dict:
        """Sincroniza cambios de stock desde plataforma externa."""
        inventory_item_id = payload.get("inventory_item_id")
        qty_available     = payload.get("available")
        logger.info(f"[Inventory] Update from {source}: item={inventory_item_id} qty={qty_available}")
        return {"status": "processed", "source": source, "qty": qty_available}

    async def _handle_product_sync(self, payload: dict, source: str) -> dict:
        """Registra cambios de producto desde plataforma externa."""
        product_id = payload.get("id")
        logger.info(f"[Product] Sync from {source}: id={product_id}")
        return {"status": "processed", "source": source, "product_id": product_id}


# ─── Facade principal ─────────────────────────────────────────────────────────

class EcommerceAgent:
    """
    Fachada principal del agente e-commerce.
    Coordina Shopify, WooCommerce y Stripe.
    """

    def __init__(self):
        self.shopify  = ShopifyConnector()
        self.woo      = WooCommerceConnector()
        self.webhooks = EcommerceWebhookHandler()

    async def sync_all_platforms(self, hb_product: dict) -> dict:
        """Sincroniza un producto a todas las plataformas configuradas."""
        results = {}

        if SHOPIFY_TOKEN and SHOPIFY_SHOP:
            try:
                results["shopify"] = await self.shopify.sync_product(hb_product)
            except Exception as e:
                results["shopify"] = {"error": str(e)}
                logger.error(f"[Shopify] sync failed: {e}")

        if WC_KEY and WC_URL:
            try:
                results["woocommerce"] = await self.woo.sync_product(hb_product)
            except Exception as e:
                results["woocommerce"] = {"error": str(e)}
                logger.error(f"[WooCommerce] sync failed: {e}")

        return results

    async def setup_webhooks(self) -> dict:
        """Registra webhooks en todas las plataformas."""
        results = {}
        if SHOPIFY_TOKEN:
            results["shopify"] = await self.shopify.register_webhooks()
        return results

    async def get_all_orders(self) -> dict:
        """Consolida pedidos de todas las plataformas."""
        orders = {}
        if SHOPIFY_TOKEN:
            orders["shopify"] = await self.shopify.get_orders()
        if WC_KEY:
            orders["woocommerce"] = await self.woo.get_orders()
        return orders


# ─── Entry point para testing ─────────────────────────────────────────────────

if __name__ == "__main__":
    import asyncio

    async def test():
        agent   = EcommerceAgent()
        product = {
            "sku": "ANI-001", "nombre": "Anillo Solitario Diamante", "categoria": "Anillos",
            "descripcion": "Anillo de compromiso en oro 18K con diamante VS1 GIA.",
            "marca": "HB Jewelry",
            "metal": {"tipo": "Oro", "quilates": 18, "peso_gramos": 3.2},
            "gemas": [{"tipo": "Diamante", "quilates_ct": 0.5, "claridad": "VS1", "color": "F", "certificado": "GIA-001"}],
            "variantes": [{"id": "ANI-001-17", "talla_mm": 17, "acabado": "Pulido", "stock": 5, "precio_usd": 850, "costo_usd": 420}],
            "precio_base_usd": 850, "publicado": True,
            "seo": {"tags": ["anillo", "diamante", "compromiso"]},
            "imagenes": [],
        }
        print(json.dumps(await agent.sync_all_platforms(product), indent=2))

    asyncio.run(test())
