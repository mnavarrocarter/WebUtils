debuild --no-tgz-check -us -uc && debuild clean
mv ../*.deb dist/
mv ../*.changes dist/
mv ../*.build dist/
mv ../*.dsc dist/
mv ../*.tar.gz dist/