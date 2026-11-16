const http = require('http');
const fs = require('fs');
const path = require('path');

const rootDir = 'C:\\Verna Developers website';
const htmlFiles = fs.readdirSync(rootDir).filter(f => f.endsWith('.html'));

console.log(`Found ${htmlFiles.length} HTML files to inspect.`);

// Check for links inside each html file
let totalLinks = 0;
let brokenLinks = 0;

for (const file of htmlFiles) {
  const content = fs.readFileSync(path.join(rootDir, file), 'utf8');
  // Match href="something"
  const regex = /href="([^"#:;]+)"/g;
  let match;
  while ((match = regex.exec(content)) !== null) {
    let link = match[1];
    // Ignore external links
    if (link.startsWith('http://') || link.startsWith('https://') || link.startsWith('//') || link.startsWith('tel:') || link.startsWith('mailto:')) {
      continue;
    }
    // Remove query params
    link = link.split('?')[0];
    if (!link) continue;
    
    // Normalize relative link
    let resolved = path.join(rootDir, link.replace(/\//g, '\\'));
    if (!fs.existsSync(resolved)) {
      // Check if it's a clean url without .html
      if (fs.existsSync(resolved + '.html')) {
        // Valid
      } else {
        console.error(`Broken link in ${file}: "${link}" -> cannot find ${resolved}`);
        brokenLinks++;
      }
    }
    totalLinks++;
  }
}

console.log(`\nLink crawl finished: inspected ${totalLinks} internal links across ${htmlFiles.length} files. Broken links: ${brokenLinks}`);
if (brokenLinks > 0) process.exit(1);

