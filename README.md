# Scraping_JavaScript_rendered_pages

selenium_projetct is study code from other source

┌───────────────────────────────────┐
│ START │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ Initialize Chrome browser (headless)│
│ Set WebDriverWait │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ For page = 1 → total_page │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ scrape_index(page) │
│ - Build index URL │
│ - browser.get(url) │
│ - Wait until .item appears │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ parse_index() │
│ - Find all <a class="name"> │
│ - Extract hrefs │
│ - Return detail_url list │
└───────────────────────────────────┘
│
▼
┌──────────────────────────────────────────────┐
│ For each detail_url in detail_urls │
└──────────────────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ scrape_detail(detail_url) │
│ - browser.get(detail_url) │
│ - Wait for <h2> to load │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ parse_detail() │
│ - name = find <h2> │
│ - categories = find .categories │
│ - score = find .score │
│ - return data tuple │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ Print / store detail_data │
└───────────────────────────────────┘
│
▼
(Loop until all detail pages)
│
▼
(Loop until all index pages)
│
▼
┌───────────────────────────────────┐
│ Close browser (quit) │
└───────────────────────────────────┘
│
▼
┌───────────────────────────────────┐
│ END │
└───────────────────────────────────┘
