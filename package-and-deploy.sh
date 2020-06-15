rm -r build
rm -r dist
rm -r "pydvdcss.egg-info"
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*