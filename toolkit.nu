# Convert files from PDF to Markdown
export def convert [...id: int] {
	poetry run python3 -m src.util.convert ...$id
}

export def render [id: int] {
	let dst_md = mktemp --tmpdir XXXXXX.md
	let dst_html = mktemp --tmpdir XXXXXX.html

	path-md $id
		| open
		| str join "\n\n---\n\n"
		| str replace --all --regex --multiline `[^|\n ]\n\|` "\n\n|"
		| str replace --all --regex --multiline `[^*\n ]\n\*` "\n\n*"
		| save --force $dst_md

	pandoc -s -o $dst_html $dst_md --metadata $"title=Document ($id)"
	rm --permanent $dst_md

	$dst_html
}

def path-md [id: int] {
	{ parent: "data/md/", stem: $id, extension: json } | path join
}
