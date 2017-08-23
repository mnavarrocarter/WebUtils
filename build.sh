debuild --no-tgz-check -us -uc && debuild clean
mv ../*.deb dist/
rm ../*.changes
rm ../*.build
rm ../*.dsc
rm ../*.tar.gz