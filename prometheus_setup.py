from prometheus_client import Counter, Histogram

VISITS = Counter(name="website_visits_total", documentation="Total visits to the website.")
MESSAGES = Counter(name="total_messages_sent", documentation="Total contact message forms submitted.")
RESUME_CLICKS = Counter(name="total_resume_clicks", documentation="Total number of clicks on download resume button.")
PORTFOLIO_VISITS = Counter(name="portfolio_page_visits", documentation="Total visits to portfolio page")
ABOUT_VISITS = Counter(name="about_page_visits", documentation="Total visits to about page.")
RESUME_VISITS = Counter(name="resume_page_visits", documentation="Total visits to resume page.")
BLOG_VISITS = Counter(name="blog_page_visits", documentation="Total visits to blog page")
EXTERNAL_CLICKS = Counter(name="external_link_clicks_total", documentation="Total clicks on external links", labelnames=["link"])
HTTP_RESPONSES = Counter(name="total_http_responses", documentation="Http reponses by status code.", labelnames=["method", "status"])
REQUEST_LATENCY = Histogram(name="http_request_latency_seconds", documentation="HTTP Request latency in seconds.", labelnames=["method", "endpoint"])