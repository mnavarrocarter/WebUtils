debuild --no-tgz-check -us -uc && debuild clean
cp ../*.deb dist/rush_latest_all.deb
mv ../*.deb dist/
rm ../*.changes
rm ../*.build
rm ../*.dsc
rm ../*.tar.gz