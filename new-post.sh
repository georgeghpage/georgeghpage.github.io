#!/usr/bin/env bash
# Create a new blog post from the template.
# Usage: ./new-post.sh my-post-slug "My post title"
set -euo pipefail
cd "$(dirname "$0")"

slug="${1:?usage: ./new-post.sh slug \"Title\"}"
title="${2:-Untitled}"
date="$(date +%F)"
file="posts/${date}-${slug}.html"

if [ -e "$file" ]; then
  echo "error: $file already exists" >&2
  exit 1
fi

sed -e "s/POST_TITLE/${title}/g" -e "s/POST_DATE/${date}/g" posts/_template.html > "$file"

echo "created $file"
echo
echo "now add this row to blog.html (top of the <ul class=\"post-list\">):"
printf '  <li><time datetime="%s">%s</time><div class="post-main"><a href="%s">%s</a></div></li>\n' "$date" "$date" "$file" "$title"
