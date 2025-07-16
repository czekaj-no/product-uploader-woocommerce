# 🛍️ product-uploader-woocommerce

Python script to bulk upload WooCommerce products with images, variations, SEO data and categories – all from a local folder and JSON file.

---

## 🚀 Features

- 🖼️ Uploads main and gallery images to `/wp-json/wp/v2/media`
- 🔐 Supports JWT authentication for secure REST API calls
- 🧾 Creates variable products with price/size variants
- ✏️ SEO-ready – supports dynamic meta data 
- 🧪 Dry-run mode to test everything safely

🔐 .env file
API_URL=https://yourstore.com/wp-json/wc/v3
API_KEY=ck_xxxxxxxx
API_SECRET=cs_xxxxxxxx

# JWT token used for media uploads
JWT_TOKEN=your.jwt.token.here
MEDIA_ENDPOINT=https://yourstore.com/wp-json/wp/v2/media
⚠️ Do not commit .env – it's excluded via .gitignore.

🧠 SEO automation
Supports placeholders like {nazwa} in SEO fields, which are replaced dynamically.

Example:

"seo_description": "High-quality poster: {nazwa}. Perfect for interiors."

📷 Image handling
Main image and gallery images are uploaded using /wp-json/wp/v2/media

Authenticated using your JWT token via Authorization: Bearer <JWT_TOKEN>

Each image receives ALT text based on its filename

🏃‍♀️ How to run

python main.py
Dry-run mode (no uploads):


dry_run = True
✅ Requirements
WooCommerce site with REST API enabled
WooCommerce API key & secret (read/write access)
JWT Auth plugin installed and working
Working /wp-json/wp/v2/media endpoint with proper JWT authorization

💡 Notes
Slugs must be unique; duplicates will be skipped
If a gallery image is missing, it is ignored (not fatal)
Variations created from warianty dict
Products are published immediately

🧼 .gitignore
.env
__pycache__/
*.pyc

🛠️ Why use this?
To stop wasting time clicking through the WP admin panel. Bulk create full-featured, SEO-optimized WooCommerce products in seconds.

