#!/bin/bash
cd dist
git init
git checkout -b gh-pages
git remote add origin $(git -C .. remote get-url origin)
git add -A
git commit -m "update"
git push -f origin gh-pages
rm -rf .git
cd ..
echo "Deployment completed successfully!"