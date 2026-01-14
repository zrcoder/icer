#!/bin/bash

# Ensure the project is built
if [ ! -d "dist" ]; then
    echo "Building project first..."
    npm run build
fi

# Clean previous build
rm -rf gh-pages-temp

# Create temp directory
mkdir -p gh-pages-temp

# Copy only the built files
cp -r dist/* gh-pages-temp/

# Create .nojekyll file for GitHub Pages
touch gh-pages-temp/.nojekyll

# Initialize git repository in temp directory if it doesn't exist
cd gh-pages-temp
if [ ! -d ".git" ]; then
    git init
    git checkout -b gh-pages 2>/dev/null || git checkout gh-pages
fi

# Add all files
git add .

# Commit changes
git commit -m "Deploy to GitHub Pages"

# Force push to gh-pages branch on origin
git push -f origin gh-pages

# Go back to root directory
cd ..

# Clean up
rm -rf gh-pages-temp

echo "Deployment completed successfully!"