import json
from config import Config
from typing import List, Dict

class MarketingCopyGenerator:
    """Generate marketing copy for HB Jewelry"""
    
    def __init__(self):
        self.config = Config
    
    def generate_copy(self, product: Dict) -> Dict:
        """Generate marketing copy for a single product"""
        
        product_name = product.get('name', 'Jewelry')
        product_type = product.get('type', 'jewelry')
        price = product.get('price', 0)
        description = product.get('description', '')
        
        # Templates for different platforms
        copies = {
            'instagram': self._generate_instagram_copy(product_name, product_type, price, description),
            'tiktok': self._generate_tiktok_copy(product_name, product_type, price, description),
            'shopify': self._generate_shopify_copy(product_name, product_type, price, description),
            'email': self._generate_email_copy(product_name, product_type, price, description)
        }
        
        return copies
    
    def _generate_instagram_copy(self, name: str, ptype: str, price: float, desc: str) -> str:
        """Instagram format: visual, engaging, hashtags"""
        return f"""✨ {name.upper()}

Diseño contemporáneo que combina con todo. Perfecto para diario o evento especial.

💎 Lujo asequible
🎨 Estilo atemporal
👥 Para todos

${price} | Link en bio

#HBJewelry #ContemporaryJewelry #JoyeriaMexico #LuxoAsequible #{ptype.title()}"""
    
    def _generate_tiktok_copy(self, name: str, ptype: str, price: float, desc: str) -> str:
        """TikTok format: hook, short, trend-friendly"""
        return f"""POV: Buscabas joyería que te durara AÑOS 💎

{name} - Solo ${price}
Diseño que va con TODO

Brilla sin pretensiones ✨
#JoyeriaContemporanea #HBJewelry #LujoAsequible"""
    
    def _generate_shopify_copy(self, name: str, ptype: str, price: float, desc: str) -> str:
        """Shopify format: SEO-friendly, benefits-focused"""
        return f"""{name} - Contemporary Jewelry

Elevate your everyday style with our {ptype} collection. Designed for the modern, discerning person who values quality and timeless aesthetics.

✓ Premium materials
✓ Versatile design
✓ Perfect for any occasion
✓ Ships within 48 hours

Price: ${price}

This piece embodies contemporary design principles while remaining accessible to everyone ages 18-45 who appreciates fine jewelry."""
    
    def _generate_email_copy(self, name: str, ptype: str, price: float, desc: str) -> str:
        """Email format: personal, conversion-focused"""
        return f"""Subject: Nueva colección: {name}

Hola,

Nos encantaría presentarte nuestro nuevo {ptype}: {name}

Diseñado con la estética contemporánea que amas, a un precio que tiene sentido.

📍 ${price}
✨ Diseño atemporal
💪 Calidad garantizada
🚚 Envío gratis

[Ver producto]

¿Preguntas? Estamos aquí.

HB Jewelry"""
    
    def generate_batch_copy(self, products: List[Dict]) -> Dict:
        """Generate copy for multiple products"""
        results = []
        
        for product in products:
            results.append({
                'product': product.get('name'),
                'copies': self.generate_copy(product)
            })
        
        return {
            'generated_copies': results,
            'total_products': len(products),
            'style': self.config.HB_JEWELRY_STYLE,
            'price_range': f"${self.config.HB_JEWELRY_PRICE_MIN}-${self.config.HB_JEWELRY_PRICE_MAX}"
        }
