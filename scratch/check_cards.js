const fs = require('fs');
const content = fs.readFileSync('index.html', 'utf8');
const regex = /<article class="govt-auth-card"[\s\S]*?<\/article>/g;
let match;
let count = 1;
while ((match = regex.exec(content)) !== null) {
  const card = match[0];
  const title = (card.match(/<h3 class="govt-auth-title">([^<]+)<\/h3>/) || [])[1];
  const src = (card.match(/src="([^"]+)"/) || [])[1];
  console.log(`${count}: ${title} => ${src}`);
  count++;
}

