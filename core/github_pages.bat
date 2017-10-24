# build the docs
cd docs
make clean
make html
cd ..

# commit and push
git add -A
git commit -m "pushing docs"
git push origin master

# switch branches and pull the data we want
git checkout gh-pages
rm -rf .
touch .nojekyll
git checkout master docs/build/html
mv ./docs/build/html/* ./
rm -rf ./docs
git add -A
git commit -m "publishing docs..."
git push origin gh-pages

# switch back
git checkout master