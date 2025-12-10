#!/bin/bash

# Check if a commit message was provided
if [ -z "$1" ]; then
  echo "Error: You must provide a commit message."
  echo "Usage: ./save_changes.sh \"Your message here\""
  exit 1
fi

echo "--- Adding changes ---"
git add .

echo "--- Committing with message: '$1' ---"
git commit -m "$1"

echo "--- Pushing to GitHub ---"
git push

echo "--- Done! ---"
