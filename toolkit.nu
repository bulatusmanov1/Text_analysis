# Convert files from PDF to Markdown
export def convert [...id: int] {
	poetry run python3 -m src.util.convert ...$id
}

export def render [id: int] {
	let dst_md = mktemp --tmpdir
	let dst_html = mktemp --tmpdir

	path-md $id
		| open
		| str join "\n\n---\n\n"
		| str replace --all --regex --multiline `[^|]\n\|` "\n\n|"
		| save --force $dst_md

	pandoc -s -o $dst_html $dst_md
	rm --permanent $dst_md

	$dst_html
}

def path-md [id: int] {
	{ parent: "data/md/", stem: $id, extension: json } | path join
}
