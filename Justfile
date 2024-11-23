run:
    uv run python cult_maker.py > output.md

book:
	pandoc --toc --top-level-division=chapter -f markdown+header_attributes -o cult.epub output.md
	pandoc --toc -V documentclass=report --top-level-division=chapter -o cult.pdf output.md

clean:
	rm -f cult.epub
	rm -f cult.pdf

pretty:
	uv run isort .
	uv run ruff format
