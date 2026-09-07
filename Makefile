.PHONY: build

build:
	python -m nuitka \
		--onefile \
		--standalone \
		--main=src \
		--output-filename=twitchpytts \
		--remove-output \
		--lto=yes \
		--strip \
		--disable-console \
		--enable-plugin=pyside6 \
		--noinclude-qt-translations \
		--include-package-data=piper \
		--include-package-data=onnxruntime \
		--include-data-dir=$$(python -c "import piper, os; print(os.path.dirname(piper.__file__))")/espeak-ng-data=espeak-ng-data